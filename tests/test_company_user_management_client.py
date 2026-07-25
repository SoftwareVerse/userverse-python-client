import pytest

from userverse_python_client.clients.company_user_management import (
    UverseCompanyUserManagementClient,
)
from userverse_models.company.user import (
    CompanyUserAddModel,
    CompanyUserRoleUpdateModel,
)
from userverse_models.user.user import UserQueryParams


def _client() -> UverseCompanyUserManagementClient:
    return UverseCompanyUserManagementClient(
        "https://example.test", access_token="token"
    )


def test_add_user_to_company_posts_payload() -> None:
    client = _client()
    add_model = CompanyUserAddModel(email="user@example.com", role="Administrator")
    called: dict[str, object] = {}

    def fake_request(method, path, json=None, **_kwargs):
        called.update(method=method, path=path, json=json)
        return {
            "data": {
                "id": "1",
                "email": "user@example.com",
                "role_name": "Administrator",
            }
        }

    client._request = fake_request  # type: ignore[method-assign]
    response = client.add_user_to_company(
        company_id="550e8400-e29b-41d4-a716-446655440000",
        user_data=add_model,
    )

    assert called == {
        "method": "POST",
        "path": "/company/550e8400-e29b-41d4-a716-446655440000/users",
        "json": add_model.model_dump(exclude_none=True),
    }
    assert response["data"]["email"] == "user@example.com"


def test_add_user_to_company_requires_dict_payload() -> None:
    client = _client()
    add_model = CompanyUserAddModel(email="user@example.com")

    def fake_request(*_args, **_kwargs):
        return {"data": []}

    client._request = fake_request  # type: ignore[method-assign]
    with pytest.raises(ValueError, match="Expected company user data"):
        client.add_user_to_company("company-id", add_model)


def test_delete_user_from_company_calls_current_endpoint() -> None:
    client = _client()
    called: dict[str, object] = {}

    def fake_request(method, path, **_kwargs):
        called.update(method=method, path=path)
        return {"data": {"id": "3", "email": "user@example.com", "role_name": "Viewer"}}

    client._request = fake_request  # type: ignore[method-assign]
    response = client.delete_user_from_company(company_id="7", user_id="3")

    assert called == {"method": "DELETE", "path": "/company/7/user/3"}
    assert response["data"]["role_name"] == "Viewer"


def test_update_user_role_calls_current_endpoint() -> None:
    client = _client()
    update_model = CompanyUserRoleUpdateModel(role="Owner")
    called: dict[str, object] = {}

    def fake_request(method, path, json=None, **_kwargs):
        called.update(method=method, path=path, json=json)
        return {"data": {"id": "3", "email": "user@example.com", "role_name": "Owner"}}

    client._request = fake_request  # type: ignore[method-assign]
    response = client.update_user_role("7", "3", update_model)

    assert called == {
        "method": "PATCH",
        "path": "/company/7/user/3",
        "json": update_model.model_dump(exclude_none=True),
    }
    assert response["data"]["role_name"] == "Owner"


def test_list_company_users_calls_endpoint() -> None:
    client = _client()
    params = UserQueryParams(limit=25, page=2)
    called: dict[str, object] = {}

    def fake_request(method, path, params=None, **_kwargs):
        called.update(method=method, path=path, params=params)
        return {
            "data": {
                "records": [{"id": "9", "email": "member@example.com"}],
                "pagination": {"limit": 25, "current_page": 2},
            }
        }

    client._request = fake_request  # type: ignore[method-assign]
    response = client.list_company_users(company_id="11", query_params=params)

    assert called == {
        "method": "GET",
        "path": "/company/11/users",
        "params": params.model_dump(exclude_none=True),
    }
    assert response["data"]["records"][0]["id"] == "9"


def test_list_company_users_requires_dict_payload() -> None:
    client = _client()
    params = UserQueryParams()

    def fake_request(*_args, **_kwargs):
        return {"data": []}

    client._request = fake_request  # type: ignore[method-assign]
    with pytest.raises(ValueError, match="Expected company user pagination data"):
        client.list_company_users("1", params)
