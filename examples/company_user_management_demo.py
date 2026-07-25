"""Demo script for managing company users through the Userverse Python client."""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Callable, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from userverse_models.company.user import (  # noqa: E402
    CompanyUserAddModel,
    CompanyUserRoleUpdateModel,
)
from userverse_models.user.user import UserLoginModel, UserQueryParams  # noqa: E402
from userverse_python_client import UverseUserClient  # noqa: E402
from userverse_python_client.clients.company_user_management import (  # noqa: E402
    UverseCompanyUserManagementClient,
)
from userverse_python_client.error_model import ClientErrorModel  # noqa: E402

BASE_URL = os.getenv("USERVERSE_BASE_URL", "https://apps.oxillium-api.co.za/userverse")

ClientProvider = Callable[[], Any]
ActionFunction = Callable[[Any], Any]


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required env var: {name}")
    return value


def build_user_client() -> UverseUserClient:
    return UverseUserClient(base_url=BASE_URL)


def build_company_user_client(token: str) -> UverseCompanyUserManagementClient:
    return UverseCompanyUserManagementClient(base_url=BASE_URL, access_token=token)


def log_response(label: str, response: Any) -> None:
    print(f"{label} Response:", response)
    dump_method = getattr(response, "model_dump", None)
    if callable(dump_method):
        print(json.dumps(dump_method(mode="json"), indent=2))


def login_user(client: UverseUserClient) -> str:
    response = client.user_login(
        UserLoginModel(
            email=require_env("USER_EMAIL"),
            password=require_env("USER_PASSWORD"),
        )
    )
    client.set_access_token(response.data.access_token)
    log_response("Login", response)
    return response.data.access_token


def build_user_query_params() -> UserQueryParams:
    params: dict[str, object] = {}
    for int_field, env_name in [
        ("limit", "COMPANY_USER_QUERY_LIMIT"),
        ("page", "COMPANY_USER_QUERY_PAGE"),
    ]:
        value = os.getenv(env_name)
        if value:
            params[int_field] = int(value)
    for field, env_name in [
        ("role_name", "COMPANY_USER_QUERY_ROLE_NAME"),
        ("first_name", "COMPANY_USER_QUERY_FIRST_NAME"),
        ("last_name", "COMPANY_USER_QUERY_LAST_NAME"),
        ("email", "COMPANY_USER_QUERY_EMAIL"),
    ]:
        value = os.getenv(env_name)
        if value:
            params[field] = value
    return UserQueryParams(**params)


def require_company_id() -> str:
    return require_env("COMPANY_USER_COMPANY_ID")


def list_company_users(client: UverseCompanyUserManagementClient) -> None:
    response = client.list_company_users(
        company_id=require_company_id(),
        query_params=build_user_query_params(),
    )
    log_response("List Company Users", response)


def add_company_user(client: UverseCompanyUserManagementClient) -> None:
    payload = CompanyUserAddModel(
        email=require_env("COMPANY_USER_ADD_EMAIL"),
        role=os.getenv("COMPANY_USER_ADD_ROLE", "Viewer"),
    )
    response = client.add_user_to_company(
        company_id=require_company_id(),
        user_data=payload,
    )
    log_response("Add Company User", response)


def update_company_user_role(client: UverseCompanyUserManagementClient) -> None:
    user_id = require_env("COMPANY_USER_UPDATE_USER_ID")
    payload = CompanyUserRoleUpdateModel(role=require_env("COMPANY_USER_UPDATE_ROLE"))
    response = client.update_user_role(
        company_id=require_company_id(),
        user_id=user_id,
        user_role=payload,
    )
    log_response("Update Company User Role", response)


def delete_company_user(client: UverseCompanyUserManagementClient) -> None:
    response = client.delete_user_from_company(
        company_id=require_company_id(),
        user_id=require_env("COMPANY_USER_DELETE_USER_ID"),
    )
    log_response("Delete Company User", response)


def run_action(
    action_name: str, fn: ActionFunction, client_provider: ClientProvider
) -> Tuple[bool, Any]:
    try:
        client = client_provider()
        result = fn(client)
        return True, result
    except ClientErrorModel as exc:
        detail = exc.payload.detail
        print(f"{action_name} failed ({exc.status_code}): {detail.message}")
        print(f"Error details: {detail.error}")
    except ValueError as exc:
        print(f"{action_name} skipped: {exc}")
    return False, None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Company user management demo")
    parser.add_argument("--login", action="store_true")
    parser.add_argument("--list-users", action="store_true")
    parser.add_argument("--add-user", action="store_true")
    parser.add_argument("--update-user-role", action="store_true")
    parser.add_argument("--delete-user", action="store_true")
    parser.add_argument("--all", action="store_true", help="Run login + list users")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    user_client = build_user_client()

    if args.all:
        args.login = True
        args.list_users = True

    access_token: Optional[str] = None
    company_user_client: Optional[UverseCompanyUserManagementClient] = None
    logged_in = False

    def get_company_user_client() -> UverseCompanyUserManagementClient:
        nonlocal company_user_client, access_token, logged_in
        if not logged_in or not access_token:
            raise ValueError("Login is required before making company user calls.")
        if company_user_client is None:
            company_user_client = build_company_user_client(access_token)
        return company_user_client

    actions = [
        ("Login", args.login, login_user, lambda: user_client, False),
        (
            "List Company Users",
            args.list_users,
            list_company_users,
            get_company_user_client,
            True,
        ),
        (
            "Add Company User",
            args.add_user,
            add_company_user,
            get_company_user_client,
            True,
        ),
        (
            "Update Company User Role",
            args.update_user_role,
            update_company_user_role,
            get_company_user_client,
            True,
        ),
        (
            "Delete Company User",
            args.delete_user,
            delete_company_user,
            get_company_user_client,
            True,
        ),
    ]

    if not any(flag for _, flag, _, _, _ in actions):
        print("No actions selected. Try --help for available options.")
        return

    for name, enabled, fn, client_provider, needs_token in actions:
        if not enabled:
            continue
        if needs_token and not logged_in:
            if args.login:
                success, token = run_action("Login", login_user, lambda: user_client)
                if not success:
                    continue
                logged_in = True
                access_token = token
                company_user_client = None
            else:
                print(f"{name} skipped: missing --login for JWT-protected call")
                continue

        success, result = run_action(name, fn, client_provider)
        if name == "Login" and success:
            logged_in = True
            access_token = result
            company_user_client = None


if __name__ == "__main__":  # pragma: no cover
    main()
