"""Small demo script showing how to use the userverse_python_client package."""

import sys
from pathlib import Path

# Allow running the example without installing the package first.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from userverse_models.user.user import (
    UserLoginModel,
    UserUpdateModel,
    UserCreateModel,
    UserReadModel,
    TokenResponseModel,
    UserQueryParams,
)
from userverse_python_client.user import UverseUserClient
from userverse_python_client.client_error import AppClientError


def test_user_login():
    """Test user login functionality."""
    user_client = UverseUserClient(base_url="https://apps.oxillium-api.co.za/userverse")
    login_model = UserLoginModel(
        email="skhendle@gmail.com",
        password="9dA(r9@xI!Z.",
    )
    try:
        response = user_client.user_login(login_model)
    except AppClientError as exc:
        detail = exc.payload.detail
        print(f"Login failed ({exc.status_code}): {detail.message}")
        print(f"Error details: {detail.error}")
        return None

    print("Login Response:", response)
    user_client.set_access_token(response.data.access_token)
    get_user = user_client.get_user()
    print("Get User Response:", get_user)
    return get_user


if __name__ == "__main__":  # pragma: no cover
    # run with uv: uv run -m examples.user_demo
    test_user_login()
