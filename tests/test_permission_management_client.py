import pytest

from userverse_models.permissions import (
    PermissionCreateModel,
    PermissionQueryParamsModel,
    PermissionUpdateModel,
)
from userverse_python_client import UversePermissionManagementClient


def _client() -> UversePermissionManagementClient:
    return UversePermissionManagementClient(
        "https://example.test", access_token="token"
    )


@pytest.mark.parametrize(
    ("method_name", "args", "expected_method", "expected_path"),
    [
        (
            "create_permission",
            (PermissionCreateModel(name="company.read", description="Read companies"),),
            "POST",
            "/permissions",
        ),
        (
            "update_permission",
            ("permission-1", PermissionUpdateModel(description="Updated")),
            "PATCH",
            "/permissions/permission-1",
        ),
        (
            "create_company_permission",
            (
                "company-1",
                PermissionCreateModel(name="invoice.read", description=None),
            ),
            "POST",
            "/company/company-1/permissions",
        ),
        (
            "update_company_permission",
            (
                "company-1",
                "permission-1",
                PermissionUpdateModel(name="invoice.approve"),
            ),
            "PATCH",
            "/company/company-1/permissions/permission-1",
        ),
    ],
)
def test_permission_payload_routes(method_name, args, expected_method, expected_path):
    client = _client()
    called = {}

    def fake_request(method, path, json=None, **_kwargs):
        called.update(method=method, path=path, json=json)
        return {
            "data": {
                "id": "permission-1",
                "name": "company.read",
                "scope": "global",
            }
        }

    client._request = fake_request  # type: ignore[method-assign]
    getattr(client, method_name)(*args)

    payload = args[-1]
    assert called == {
        "method": expected_method,
        "path": expected_path,
        "json": payload.model_dump(exclude_none=True),
    }


@pytest.mark.parametrize(
    ("method_name", "args", "expected_path"),
    [
        ("get_permissions", (), "/permissions"),
        ("get_company_permissions", ("company-1",), "/company/company-1/permissions"),
    ],
)
def test_permission_list_routes_send_query_params(method_name, args, expected_path):
    client = _client()
    params = PermissionQueryParamsModel(limit=25, page=2, name="read")
    called = {}

    def fake_request(method, path, params=None, **_kwargs):
        called.update(method=method, path=path, params=params)
        return {"data": {"records": [], "pagination": {}}}

    client._request = fake_request  # type: ignore[method-assign]
    getattr(client, method_name)(*args, params)

    assert called == {
        "method": "GET",
        "path": expected_path,
        "params": params.model_dump(exclude_none=True),
    }


@pytest.mark.parametrize(
    (
        "method_name",
        "args",
        "expected_method",
        "expected_path",
        "response_data",
    ),
    [
        (
            "delete_permission",
            ("permission-1",),
            "DELETE",
            "/permissions/permission-1",
            {"id": "permission-1"},
        ),
        (
            "get_role_permissions",
            ("role-1",),
            "GET",
            "/roles/role-1/permissions",
            [],
        ),
        (
            "assign_permission_to_role",
            ("role-1", "permission-1"),
            "POST",
            "/roles/role-1/permissions/permission-1",
            {"id": "role-1", "permissions": []},
        ),
        (
            "remove_permission_from_role",
            ("role-1", "permission-1"),
            "DELETE",
            "/roles/role-1/permissions/permission-1",
            {"id": "role-1", "permissions": []},
        ),
        (
            "delete_company_permission",
            ("company-1", "permission-1"),
            "DELETE",
            "/company/company-1/permissions/permission-1",
            {"id": "permission-1"},
        ),
        (
            "get_company_role_permissions",
            ("company-1", "role-1"),
            "GET",
            "/company/company-1/roles/role-1/permissions",
            [],
        ),
        (
            "assign_company_permission_to_role",
            ("company-1", "role-1", "permission-1"),
            "POST",
            "/company/company-1/roles/role-1/permissions/permission-1",
            {"id": "role-1", "permissions": []},
        ),
        (
            "remove_company_permission_from_role",
            ("company-1", "role-1", "permission-1"),
            "DELETE",
            "/company/company-1/roles/role-1/permissions/permission-1",
            {"id": "role-1", "permissions": []},
        ),
    ],
)
def test_permission_assignment_routes(
    method_name, args, expected_method, expected_path, response_data
):
    client = _client()
    called = {}

    def fake_request(method, path, **_kwargs):
        called.update(method=method, path=path)
        return {"data": response_data}

    client._request = fake_request  # type: ignore[method-assign]
    getattr(client, method_name)(*args)

    assert called == {"method": expected_method, "path": expected_path}


def test_permission_methods_reject_invalid_response_shape():
    client = _client()
    client._request = lambda *_args, **_kwargs: {"data": []}  # type: ignore[method-assign]

    with pytest.raises(ValueError, match="create permission data to be dict"):
        client.create_permission(PermissionCreateModel(name="company.read"))
