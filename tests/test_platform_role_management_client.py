import pytest

from userverse_python_client import UversePlatformRoleManagementClient


@pytest.mark.parametrize(
    ("method_name", "args", "expected_method", "expected_path"),
    [
        ("get_user_roles", ("user-1",), "GET", "/users/user-1/roles"),
        (
            "assign_role_to_user",
            ("user-1", "role-1"),
            "POST",
            "/users/user-1/roles/role-1",
        ),
        (
            "remove_role_from_user",
            ("user-1", "role-1"),
            "DELETE",
            "/users/user-1/roles/role-1",
        ),
    ],
)
def test_platform_role_routes(method_name, args, expected_method, expected_path):
    client = UversePlatformRoleManagementClient(
        "https://example.test", access_token="token"
    )
    called = {}

    def fake_request(method, path, **_kwargs):
        called.update(method=method, path=path)
        return {"data": [{"id": "role-1", "name": "Admin", "permissions": []}]}

    client._request = fake_request  # type: ignore[method-assign]
    getattr(client, method_name)(*args)

    assert called == {"method": expected_method, "path": expected_path}


def test_platform_role_methods_require_list_data():
    client = UversePlatformRoleManagementClient("https://example.test", "token")
    client._request = lambda *_args, **_kwargs: {"data": {}}  # type: ignore[method-assign]

    with pytest.raises(ValueError, match="data to be a list"):
        client.get_user_roles("user-1")
