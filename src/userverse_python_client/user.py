import base64

from sverse_generic_models.generic_response import GenericResponseModel
from userverse_models.user.user import (
    UserLoginModel,
    UserUpdateModel,
    UserCreateModel,
    UserReadModel,
    TokenResponseModel,
    UserQueryParams,
)
from .http_client_base import BaseClient


class UverseUserClient(BaseClient):

    def _encode_basic_auth(self, email: str, password: str) -> str:
        """Encodes email and password into a Basic Auth header string."""
        credentials = f"{email}:{password}"
        encoded_bytes = base64.b64encode(credentials.encode("utf-8"))
        return f"Basic {encoded_bytes.decode('utf-8')}"

    def user_login(
        self, user_login: UserLoginModel
    ) -> GenericResponseModel[TokenResponseModel]:
        """Logs in a user using Basic Auth and returns the response data."""
        basic_auth = self._encode_basic_auth(user_login.email, user_login.password)
        headers = {"Authorization": basic_auth}

        # Userverse login uses Basic Auth with a PATCH request.
        response = self._request("PATCH", "/user/login", headers=headers)

        if not response or "data" not in response:
            raise ValueError("Invalid response from login endpoint")

        return GenericResponseModel[TokenResponseModel].model_validate(response)

    def create_user(
        self, user_data: UserCreateModel
    ) -> GenericResponseModel[UserReadModel]:
        """Creates a new user with the provided data and returns the user model."""
        response = self._request("POST", "/user", json=user_data)

        if not response or "data" not in response:
            raise ValueError("Invalid response from create user endpoint")

        data = response.get("data", {})
        if not isinstance(data, dict):
            raise ValueError(f"Expected user data to be a dict, got {type(data)}")

        return GenericResponseModel[UserReadModel].model_validate(response)

    def get_user(self) -> GenericResponseModel[UserReadModel]:
        """Retrieves the current user's details."""
        response = self._request("GET", "/user/get")
        if not response:
            raise ValueError("No user data found in response")
        if not isinstance(response, dict):
            raise ValueError(f"Expected user data to be a dict, got {type(response)}")
        return GenericResponseModel[UserReadModel].model_validate(response)
