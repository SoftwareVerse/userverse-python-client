import requests
from typing import Any, Dict, Optional

# Todo: create models for those imports
from .models.enums import Errors
from .models.exceptions import AppError


class BaseClient:
    def __init__(
        self,
        base_url: str,
        access_token: Optional[str] = None,
        timeout: int = 30,
    ):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )
        self.timeout = timeout

        if access_token:
            self.set_access_token(access_token)

    def set_access_token(self, token: str) -> None:
        """
        Update (or add) the Authorization header for all future requests.
        """
        # note: 'bearer' lowercase is fine, but either works
        self.session.headers["Authorization"] = f"bearer {token}"

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        if not path.startswith("/"):
            raise ValueError("Path must start with '/'")

        url = f"{self.base_url}{path}"
        try:
            resp = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                headers=headers,
                timeout=self.timeout,
            )
            # this will raise requests.exceptions.HTTPError for 4xx/5xx
            resp.raise_for_status()
            return resp.json()

        except requests.exceptions.HTTPError as http_err:
            # http_err.response is the Response object
            status = http_err.response.status_code
            content = (
                http_err.response.json() if http_err.response.content else "No content"
            )
            # re-wrap or re-raise, embedding status/content if you like
            raise AppError(
                status_code=status,
                message=Errors.INVALID_REQUEST_MESSAGE.value,
                error=content,
            ) from http_err

        except Exception as e:
            # fallback for non-HTTP errors (network issues, timeouts, etc.)
            raise AppError(
                status_code=500,
                message=Errors.INVALID_REQUEST_MESSAGE.value,
                error=str(e),
            ) from e