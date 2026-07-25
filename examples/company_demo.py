"""Demo script showing how to use the company client."""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Callable, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from userverse_models.company.address import CompanyAddressModel  # noqa: E402
from userverse_models.company.company import (  # noqa: E402
    CompanyCreateModel,
    CompanyQueryParamsModel,
    CompanyUpdateModel,
)
from userverse_models.user.user import UserLoginModel  # noqa: E402
from userverse_python_client import UverseCompanyClient, UverseUserClient  # noqa: E402
from userverse_python_client.error_model import ClientErrorModel  # noqa: E402

BASE_URL = os.getenv("USERVERSE_BASE_URL", "https://apps.oxillium-api.co.za/userverse")
USE_ENV_VALUE = object()

ClientProvider = Callable[[], Any]
ActionFunction = Callable[[Any], Any]


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required env var: {name}")
    return value


def build_user_client() -> UverseUserClient:
    return UverseUserClient(base_url=BASE_URL)


def build_company_client(token: str) -> UverseCompanyClient:
    return UverseCompanyClient(base_url=BASE_URL, access_token=token)


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


def build_query_params() -> CompanyQueryParamsModel:
    params: dict[str, object] = {}
    for int_field, env_name in [("limit", "COMPANY_QUERY_LIMIT"), ("page", "COMPANY_QUERY_PAGE")]:
        value = os.getenv(env_name)
        if value:
            params[int_field] = int(value)
    for field, env_name in [
        ("role_name", "COMPANY_QUERY_ROLE_NAME"),
        ("name", "COMPANY_QUERY_NAME"),
        ("description", "COMPANY_QUERY_DESCRIPTION"),
        ("industry", "COMPANY_QUERY_INDUSTRY"),
        ("email", "COMPANY_QUERY_EMAIL"),
    ]:
        value = os.getenv(env_name)
        if value:
            params[field] = value
    return CompanyQueryParamsModel(**params)


def parse_address(prefix: str) -> Optional[CompanyAddressModel]:
    raw_json = os.getenv(f"{prefix}_ADDRESS_JSON")
    if raw_json:
        return CompanyAddressModel.model_validate_json(raw_json)

    data = {
        "street": os.getenv(f"{prefix}_ADDRESS_STREET"),
        "city": os.getenv(f"{prefix}_ADDRESS_CITY"),
        "state": os.getenv(f"{prefix}_ADDRESS_STATE"),
        "postal_code": os.getenv(f"{prefix}_ADDRESS_POSTAL_CODE"),
        "country": os.getenv(f"{prefix}_ADDRESS_COUNTRY"),
    }
    data = {key: value for key, value in data.items() if value}
    return CompanyAddressModel(**data) if data else None


def list_user_companies(client: UverseCompanyClient) -> None:
    log_response("List Companies", client.get_user_companies(build_query_params()))


def get_company_by_id(client: UverseCompanyClient, company_id_value: object = USE_ENV_VALUE) -> None:
    company_id = require_env("COMPANY_LOOKUP_ID") if company_id_value is USE_ENV_VALUE else str(company_id_value)
    log_response("Company Lookup (ID)", client.get_company_by_id_or_email(company_id=company_id))


def get_company_by_email(client: UverseCompanyClient, email_value: object = USE_ENV_VALUE) -> None:
    email = require_env("COMPANY_LOOKUP_EMAIL") if email_value is USE_ENV_VALUE else str(email_value)
    log_response("Company Lookup (Email)", client.get_company_by_id_or_email(email=email))


def create_company(client: UverseCompanyClient) -> None:
    payload = CompanyCreateModel(
        name=require_env("COMPANY_CREATE_NAME"),
        email=require_env("COMPANY_CREATE_EMAIL"),
        description=os.getenv("COMPANY_CREATE_DESCRIPTION"),
        industry=os.getenv("COMPANY_CREATE_INDUSTRY"),
        phone_number=os.getenv("COMPANY_CREATE_PHONE_NUMBER"),
        address=parse_address("COMPANY_CREATE"),
    )
    log_response("Create Company", client.create_company(payload))


def update_company(client: UverseCompanyClient) -> None:
    company_id = require_env("COMPANY_UPDATE_ID")
    payload = CompanyUpdateModel(
        name=os.getenv("COMPANY_UPDATE_NAME"),
        description=os.getenv("COMPANY_UPDATE_DESCRIPTION"),
        industry=os.getenv("COMPANY_UPDATE_INDUSTRY"),
        phone_number=os.getenv("COMPANY_UPDATE_PHONE_NUMBER"),
        address=parse_address("COMPANY_UPDATE"),
    )
    if not payload.model_dump(exclude_none=True):
        raise ValueError("Provide at least one COMPANY_UPDATE_* value to update.")
    log_response("Update Company", client.update_company(company_id, payload))


def run_action(action_name: str, fn: ActionFunction, client_provider: ClientProvider) -> Tuple[bool, Any]:
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
    parser = argparse.ArgumentParser(description="Userverse company demo")
    parser.add_argument("--login", action="store_true")
    parser.add_argument("--list-companies", action="store_true")
    parser.add_argument("--get-company-by-id", metavar="COMPANY_ID", nargs="?", const=USE_ENV_VALUE)
    parser.add_argument("--get-company-by-email", metavar="COMPANY_EMAIL", nargs="?", const=USE_ENV_VALUE)
    parser.add_argument("--create-company", action="store_true")
    parser.add_argument("--update-company", action="store_true")
    parser.add_argument("--all", action="store_true", help="Run login + list companies")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    user_client = build_user_client()

    if args.all:
        args.login = True
        args.list_companies = True

    access_token: Optional[str] = None
    company_client: Optional[UverseCompanyClient] = None
    logged_in = False

    def get_company_client() -> UverseCompanyClient:
        nonlocal company_client, access_token, logged_in
        if not logged_in or not access_token:
            raise ValueError("Login is required before making company API calls.")
        if company_client is None:
            company_client = build_company_client(access_token)
        return company_client

    actions = [
        ("Login", args.login, login_user, lambda: user_client, False),
        ("List Companies", args.list_companies, list_user_companies, get_company_client, True),
        (
            "Get Company (ID)",
            args.get_company_by_id is not None,
            lambda client, value=args.get_company_by_id: get_company_by_id(client, value),
            get_company_client,
            True,
        ),
        (
            "Get Company (Email)",
            args.get_company_by_email is not None,
            lambda client, value=args.get_company_by_email: get_company_by_email(client, value),
            get_company_client,
            True,
        ),
        ("Create Company", args.create_company, create_company, get_company_client, True),
        ("Update Company", args.update_company, update_company, get_company_client, True),
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
                company_client = None
            else:
                print(f"{name} skipped: missing --login for JWT-protected call")
                continue

        success, result = run_action(name, fn, client_provider)
        if name == "Login" and success:
            logged_in = True
            access_token = result
            company_client = None


if __name__ == "__main__":  # pragma: no cover
    main()
