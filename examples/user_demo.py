"""Demo script showing how to use the userverse user client."""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from userverse_models.user.password import (  # noqa: E402
    MagicLinkPasswordResetConfirmRequest,
    PasswordResetRequest,
)
from userverse_models.user.user import (  # noqa: E402
    RefreshTokenRequestModel,
    UserCreateModel,
    UserLoginModel,
    UserUpdateModel,
)
from userverse_python_client import UverseUserClient  # noqa: E402
from userverse_python_client.error_model import ClientErrorModel  # noqa: E402

BASE_URL = os.getenv("USERVERSE_BASE_URL", "https://apps.oxillium-api.co.za/userverse")


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required env var: {name}")
    return value


def build_client() -> UverseUserClient:
    return UverseUserClient(base_url=BASE_URL)


def login_user(client: UverseUserClient) -> str:
    response = client.user_login(
        UserLoginModel(
            email=require_env("USER_EMAIL"),
            password=require_env("USER_PASSWORD"),
        )
    )
    client.set_access_token(response.data.access_token)
    print("Login Response:", response)
    return response.data.access_token


def create_user(client: UverseUserClient) -> None:
    user_data = UserCreateModel(
        first_name=os.getenv("NEW_USER_FIRST_NAME"),
        last_name=os.getenv("NEW_USER_LAST_NAME"),
        phone_number=os.getenv("NEW_USER_PHONE_NUMBER"),
    )
    user_credentials = UserLoginModel(
        email=require_env("NEW_USER_EMAIL"),
        password=require_env("NEW_USER_PASSWORD"),
    )
    response = client.create_user(user_data, user_credentials)
    print("Create User Response:", response)


def refresh_token(client: UverseUserClient) -> None:
    response = client.refresh_user_token(
        RefreshTokenRequestModel(refresh_token=require_env("USER_REFRESH_TOKEN"))
    )
    client.set_access_token(response.data.access_token)
    print("Refresh Token Response:", response)


def revoke_token(client: UverseUserClient) -> None:
    response = client.revoke_refresh_token(
        RefreshTokenRequestModel(refresh_token=require_env("USER_REFRESH_TOKEN"))
    )
    print("Revoke Token Response:", response)


def get_user(client: UverseUserClient) -> None:
    print("Get User Response:", client.get_user())


def update_user(client: UverseUserClient) -> None:
    update = UserUpdateModel(
        first_name=os.getenv("UPDATE_FIRST_NAME"),
        last_name=os.getenv("UPDATE_LAST_NAME"),
        phone_number=os.getenv("UPDATE_PHONE_NUMBER"),
        password=os.getenv("UPDATE_PASSWORD"),
    )
    print("Update User Response:", client.update_user(update))


def resend_verification_email(client: UverseUserClient) -> None:
    payload = PasswordResetRequest(email=require_env("VERIFY_EMAIL"))
    print(
        "Resend Verification Response:",
        client.resend_verification_email(payload),
    )


def verify_user(client: UverseUserClient) -> None:
    print("Verify User Response:", client.verify_user(require_env("VERIFY_TOKEN")))


def request_password_reset(client: UverseUserClient) -> None:
    payload = PasswordResetRequest(
        email=require_env("RESET_EMAIL"),
        method=os.getenv("RESET_METHOD", "otp"),
    )
    print("Password Reset Request Response:", client.request_password_reset(payload))


def reset_password_with_otp(client: UverseUserClient) -> None:
    response = client.reset_password_validate_otp(
        UserLoginModel(
            email=require_env("RESET_EMAIL"),
            password=require_env("RESET_NEW_PASSWORD"),
        ),
        one_time_pin=require_env("RESET_OTP"),
    )
    print("Password Reset OTP Response:", response)


def reset_password_with_token(client: UverseUserClient) -> None:
    response = client.reset_password_with_token(
        MagicLinkPasswordResetConfirmRequest(
            token=require_env("RESET_TOKEN"),
            new_password=require_env("RESET_NEW_PASSWORD"),
        )
    )
    print("Password Reset Token Response:", response)


def delete_user(client: UverseUserClient) -> None:
    print("Delete User Response:", client.delete_user())


def run_action(action_name: str, fn, client: UverseUserClient) -> bool:
    try:
        fn(client)
        return True
    except ClientErrorModel as exc:
        detail = exc.payload.detail
        print(f"{action_name} failed ({exc.status_code}): {detail.message}")
        print(f"Error details: {detail.error}")
    except ValueError as exc:
        print(f"{action_name} skipped: {exc}")
    return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Userverse user demo")
    parser.add_argument("--login", action="store_true")
    parser.add_argument("--create-user", action="store_true")
    parser.add_argument("--refresh-token", action="store_true")
    parser.add_argument("--revoke-token", action="store_true")
    parser.add_argument("--get-user", action="store_true")
    parser.add_argument("--update-user", action="store_true")
    parser.add_argument("--resend-verification", action="store_true")
    parser.add_argument("--verify-user", action="store_true")
    parser.add_argument("--request-password-reset", action="store_true")
    parser.add_argument("--reset-password-otp", action="store_true")
    parser.add_argument("--reset-password-token", action="store_true")
    parser.add_argument("--delete-user", action="store_true")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run login + get-user + update-user",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client = build_client()

    if args.all:
        args.login = True
        args.get_user = True
        args.update_user = True

    actions = [
        ("Login", args.login, login_user, False),
        ("Create User", args.create_user, create_user, False),
        ("Refresh Token", args.refresh_token, refresh_token, False),
        ("Revoke Token", args.revoke_token, revoke_token, False),
        ("Get User", args.get_user, get_user, True),
        ("Update User", args.update_user, update_user, True),
        (
            "Resend Verification",
            args.resend_verification,
            resend_verification_email,
            False,
        ),
        ("Verify User", args.verify_user, verify_user, False),
        (
            "Request Password Reset",
            args.request_password_reset,
            request_password_reset,
            False,
        ),
        ("Reset Password OTP", args.reset_password_otp, reset_password_with_otp, False),
        (
            "Reset Password Token",
            args.reset_password_token,
            reset_password_with_token,
            False,
        ),
        ("Delete User", args.delete_user, delete_user, True),
    ]

    if not any(flag for _, flag, _, _ in actions):
        print("No actions selected. Try --help for available options.")
        return

    logged_in = False
    for name, enabled, fn, needs_token in actions:
        if not enabled:
            continue
        if needs_token and not logged_in:
            if args.login:
                logged_in = run_action("Login", login_user, client)
            else:
                print(f"{name} skipped: missing --login for JWT-protected call")
                continue
        action_ok = run_action(name, fn, client)
        if name == "Login":
            logged_in = action_ok


if __name__ == "__main__":  # pragma: no cover
    main()
