import base64

from sverse_generic_models.generic_response import GenericResponseModel
from userverse_models.user.user import (
    RefreshTokenRequestModel,
    TokenRevocationResponseModel,
    UserLoginModel,
    UserUpdateModel,
    UserCreateModel,
    UserReadModel,
    TokenResponseModel,
)
from userverse_models.user.password import (
    MagicLinkPasswordResetConfirmRequest,
    PasswordResetRequest,
)
from ..http_client_base import BaseClient


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
        self,
        user_data: UserCreateModel,
        user_credentials: UserLoginModel,
    ) -> GenericResponseModel[UserReadModel]:
        """Creates a new user with the provided data and Basic Auth, returns the user model."""
        basic_auth = self._encode_basic_auth(
            user_credentials.email, user_credentials.password
        )
        headers = {"Authorization": basic_auth}

        response = self._request("POST", "/user/create", json=user_data, headers=headers)

        if not response or "data" not in response:
            raise ValueError("Invalid response from create user endpoint")

        data = response.get("data", {})
        if not isinstance(data, dict):
            raise ValueError(f"Expected user data to be a dict, got {type(data)}")

        return GenericResponseModel[UserReadModel].model_validate(response)

    def refresh_user_token(
        self, payload: RefreshTokenRequestModel
    ) -> GenericResponseModel[TokenResponseModel]:
        """Refreshes access and refresh tokens using a refresh token."""
        response = self._request("POST", "/user/refresh", json=payload)

        if not response or "data" not in response:
            raise ValueError("Invalid response from refresh user token endpoint")

        return GenericResponseModel[TokenResponseModel].model_validate(response)

    def revoke_refresh_token(
        self, payload: RefreshTokenRequestModel
    ) -> GenericResponseModel[TokenRevocationResponseModel]:
        """Revokes the provided refresh token family."""
        response = self._request("POST", "/user/revoke", json=payload)

        if not response or "data" not in response:
            raise ValueError("Invalid response from revoke refresh token endpoint")

        return GenericResponseModel[TokenRevocationResponseModel].model_validate(
            response
        )

    def get_user(self) -> GenericResponseModel[UserReadModel]:
        """Retrieves the current user's details. JWT token must be set in the client."""
        response = self._request("GET", "/user/get")
        if not response:
            raise ValueError("No user data found in response")
        if not isinstance(response, dict):
            raise ValueError(f"Expected user data to be a dict, got {type(response)}")
        return GenericResponseModel[UserReadModel].model_validate(response)

    def update_user(
        self, user_update: UserUpdateModel
    ) -> GenericResponseModel[UserReadModel]:
        """Updates the current user's details. JWT token must be set in the client."""
        response = self._request("PATCH", "/user/update", json=user_update)
        if not response:
            raise ValueError("No user data found in response")
        if not isinstance(response, dict):
            raise ValueError(f"Expected user data to be a dict, got {type(response)}")
        return GenericResponseModel[UserReadModel].model_validate(response)

    # Account verification methods
    def resend_verification_email(
        self, payload: PasswordResetRequest
    ) -> GenericResponseModel[None]:
        """Resends the verification email to the provided email address."""
        response = self._request("POST", "/user/resend-verification", json=payload)
        if not response:
            raise ValueError("No data found in response")
        if not isinstance(response, dict):
            raise ValueError(
                f"Expected response data to be a dict, got {type(response)}"
            )
        return GenericResponseModel[None].model_validate(response)

    def verify_user(self, token: str) -> GenericResponseModel[None]:
        """Verifies the current user's email. Token sent via email."""
        path = self._build_path_with_query("/user/verify", {"token": token})
        response = self._request("GET", path)
        if not response:
            raise ValueError("No data found in response")
        if not isinstance(response, dict):
            raise ValueError(
                f"Expected response data to be a dict, got {type(response)}"
            )
        return GenericResponseModel[None].model_validate(response)

    # Password reset methods
    def request_password_reset(
        self, payload: PasswordResetRequest
    ) -> GenericResponseModel[None]:
        """Requests a password reset using the configured reset method."""
        response = self._request("PATCH", "/password-reset/request", json=payload)
        if not response:
            raise ValueError("No data found in response")
        if not isinstance(response, dict):
            raise ValueError(
                f"Expected response data to be a dict, got {type(response)}"
            )
        return GenericResponseModel[None].model_validate(response)

    def reset_password_with_token(
        self, payload: MagicLinkPasswordResetConfirmRequest
    ) -> GenericResponseModel[None]:
        """Resets a password using a magic-link token."""
        response = self._request(
            "PATCH", "/password-reset/reset-with-token", json=payload
        )
        if not response:
            raise ValueError("No data found in response")
        if not isinstance(response, dict):
            raise ValueError(
                f"Expected response data to be a dict, got {type(response)}"
            )
        return GenericResponseModel[None].model_validate(response)

    def reset_password_validate_otp(
        self, user_credentials: UserLoginModel, one_time_pin: str
    ) -> GenericResponseModel[None]:
        """Resets the user's password using OTP and Basic Auth."""
        basic_auth = self._encode_basic_auth(
            user_credentials.email, user_credentials.password
        )
        headers = {"Authorization": basic_auth}
        path = self._build_path_with_query(
            "/password-reset/validate-otp", {"one_time_pin": one_time_pin}
        )

        response = self._request("PATCH", path, headers=headers)

        if not response:
            raise ValueError("No data found in response")
        if not isinstance(response, dict):
            raise ValueError(
                f"Expected response data to be a dict, got {type(response)}"
            )

        return GenericResponseModel[None].model_validate(response)

    def delete_user(self) -> GenericResponseModel[None]:
        """Deletes the authenticated user's account."""
        response = self._request("DELETE", "/user/me")
        if not response:
            raise ValueError("No data found in response")
        if not isinstance(response, dict):
            raise ValueError(
                f"Expected response data to be a dict, got {type(response)}"
            )
        return GenericResponseModel[None].model_validate(response)
