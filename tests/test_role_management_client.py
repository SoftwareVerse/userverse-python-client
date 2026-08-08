import pytest

from userverse_models.company.roles import (
    RoleAssignCompaniesModel,
    RoleCreateModel,
    RoleQueryParamsModel,
    RoleUpdateModel,
)
from userverse_python_client import UverseRoleManagementClient


def _client() -> UverseRoleManagementClient:
    return UverseRoleManagementClient("https://example.test", access_token="token")


def test_create_role_posts_typed_payload():
    client = _client()
    payload = RoleCreateModel(name="Auditor", description="Read audit records")
    called = {}

    def fake_request(method, path, json=None, **_kwargs):
        called.update(method=method, path=path, json=json)
        return {"data": {"id": "role-1", "name": "Auditor", "permissions": []}}

    client._request = fake_request  # type: ignore[method-assign]
    client.create_role(payload)

    assert called == {
        "method": "POST",
        "path": "/roles",
        "json": payload.model_dump(exclude_none=True),
    }


def test_get_roles_sends_query_parameters():
    client = _client()
    params = RoleQueryParamsModel(limit=5, page=2, name="Audit")
    called = {}

    def fake_request(method, path, params=None, **_kwargs):
        called.update(method=method, path=path, params=params)
        return {"data": {"records": [], "pagination": {}}}

    client._request = fake_request  # type: ignore[method-assign]
    client.get_roles(params)

    assert called == {
        "method": "GET",
        "path": "/roles",
        "params": params.model_dump(exclude_none=True),
    }


def test_update_role_patches_typed_payload():
    client = _client()
    payload = RoleUpdateModel(name="Reviewer", description=None)
    called = {}

    def fake_request(method, path, json=None, **_kwargs):
        called.update(method=method, path=path, json=json)
        return {"data": {"id": "role-1", "name": "Reviewer", "permissions": []}}

    client._request = fake_request  # type: ignore[method-assign]
    client.update_role("role-1", payload)

    assert called == {
        "method": "PATCH",
        "path": "/roles/role-1",
        "json": payload.model_dump(exclude_none=True),
    }


def test_bulk_assign_role_posts_company_ids():
    client = _client()
    payload = RoleAssignCompaniesModel(company_ids=["company-1", "company-2"])
    called = {}

    def fake_request(method, path, json=None, **_kwargs):
        called.update(method=method, path=path, json=json)
        return {"data": {"role_id": "role-1", "company_ids": payload.company_ids}}

    client._request = fake_request  # type: ignore[method-assign]
    client.assign_role_to_companies("role-1", payload)

    assert called == {
        "method": "POST",
        "path": "/roles/role-1/companies",
        "json": payload.model_dump(exclude_none=True),
    }


@pytest.mark.parametrize(
    ("method_name", "args", "expected_method", "expected_path", "response_data"),
    [
        ("delete_role", ("role-1",), "DELETE", "/roles/role-1", {"id": "role-1"}),
        (
            "assign_role_to_company",
            ("company-1", "role-1"),
            "POST",
            "/company/company-1/roles/role-1",
            {"id": "role-1", "permissions": []},
        ),
        (
            "unassign_role_from_company",
            ("company-1", "role-1"),
            "DELETE",
            "/company/company-1/roles/role-1",
            {"role_id": "role-1"},
        ),
    ],
)
def test_role_assignment_routes(
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


def test_role_methods_reject_invalid_response_shape():
    client = _client()
    client._request = lambda *_args, **_kwargs: {"data": []}  # type: ignore[method-assign]

    with pytest.raises(ValueError, match="create role data to be dict"):
        client.create_role(RoleCreateModel(name="Auditor", description=None))
