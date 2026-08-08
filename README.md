[![CI - Release Tag](https://github.com/SoftwareVerse/userverse-python-client/actions/workflows/release.yml/badge.svg)](https://github.com/SoftwareVerse/userverse-python-client/actions/workflows/release.yml)
[![Latest Release](https://img.shields.io/github/v/release/SoftwareVerse/userverse-python-client?display_name=tag&sort=semver)](https://github.com/SoftwareVerse/userverse-python-client/releases/latest)
[![Latest Tag](https://img.shields.io/github/v/tag/SoftwareVerse/userverse-python-client?label=tag&sort=semver)](https://github.com/SoftwareVerse/userverse-python-client/releases/latest)
[![Release Date](https://img.shields.io/github/release-date/SoftwareVerse/userverse-python-client)](https://github.com/SoftwareVerse/userverse-python-client/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/SoftwareVerse/userverse-python-client/total)](https://github.com/SoftwareVerse/userverse-python-client/releases)
[![codecov](https://codecov.io/gh/SoftwareVerse/userverse-python-client/branch/main/graph/badge.svg?token=YOUR_TOKEN)](https://codecov.io/gh/SoftwareVerse/userverse-python-client)

# userverse-python-client

Python SDK for the Userverse HTTP API.

## What This SDK Covers

The current client surface matches the Userverse API routes for:

- user login, create, profile update, verification, refresh, revoke, and delete
- password reset by OTP or magic link
- user company listing
- company create, lookup, and update
- company membership listing, add, remove, and role update
- company role listing, create, update, delete, and built-in role discovery
- global role management and company role assignments
- global and company-scoped permission management
- platform role assignments and effective user permissions

## Installation

Install from PyPI:

```bash
python -m pip install userverse-python-client
```

Install from source:

```bash
git clone https://github.com/SoftwareVerse/userverse-python-client.git
cd userverse-python-client
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Quick Start

```python
from userverse_python_client import UverseUserClient
from userverse_models.user.user import UserLoginModel

base_url = "https://your-api-host/userverse"

user_client = UverseUserClient(base_url=base_url)
login = user_client.user_login(
    UserLoginModel(
        email="user@example.com",
        password="secret",
    )
)

access_token = login.data.access_token
user_client.set_access_token(access_token)

profile = user_client.get_user()
print(profile.data.email)
```

## Client Overview

### `UverseUserClient`

Use for:

- `user_login`
- `create_user`
- `refresh_user_token`
- `revoke_refresh_token`
- `get_user`
- `update_user`
- `resend_verification_email`
- `verify_user`
- `request_password_reset`
- `reset_password_with_token`
- `reset_password_validate_otp`
- `delete_user`

### `UverseCompanyClient`

Use for:

- `get_user_companies`
- `get_company_by_id_or_email`
- `create_company`
- `update_company`

### `UverseCompanyUserManagementClient`

Use for:

- `list_company_users`
- `add_user_to_company`
- `delete_user_from_company`
- `update_user_role`

### `UverseCompanyUserRolesManagement`

Use for:

- `get_company_roles`
- `create_company_role`
- `update_company_role`
- `delete_company_role`
- `list_default_roles`

### `UverseRoleManagementClient`

Use for:

- `create_role`, `get_roles`, `update_role`, and `delete_role`
- `assign_role_to_companies`
- `assign_role_to_company` and `unassign_role_from_company`

### `UversePermissionManagementClient`

Use for:

- global permission create, list, update, and delete operations
- company permission create, list, update, and delete operations
- listing, assigning, and removing permissions from global or company roles

### `UversePlatformRoleManagementClient`

Use for:

- `get_user_roles`
- `assign_role_to_user`
- `remove_role_from_user`

`UverseUserClient.get_user_permissions()` returns the current user's effective
platform permissions.

## Typical Flows

### User auth and profile

```python
from userverse_python_client import UverseUserClient
from userverse_models.user.user import UserLoginModel, UserUpdateModel

client = UverseUserClient("https://your-api-host/userverse")

login = client.user_login(UserLoginModel(email="user@example.com", password="secret"))
client.set_access_token(login.data.access_token)

updated = client.update_user(
    UserUpdateModel(first_name="Updated", phone_number="+27821234567")
)
```

### Refresh and revoke tokens

```python
from userverse_models.user.user import RefreshTokenRequestModel

refresh = client.refresh_user_token(
    RefreshTokenRequestModel(refresh_token="refresh-token")
)

revoked = client.revoke_refresh_token(
    RefreshTokenRequestModel(refresh_token="refresh-token")
)
```

### Password reset

```python
from userverse_models.user.password import (
    PasswordResetRequest,
    MagicLinkPasswordResetConfirmRequest,
)
from userverse_models.user.user import UserLoginModel

client.request_password_reset(
    PasswordResetRequest(email="user@example.com", method="otp")
)

client.reset_password_validate_otp(
    UserLoginModel(email="user@example.com", password="new-password"),
    one_time_pin="123456",
)

client.request_password_reset(
    PasswordResetRequest(email="user@example.com", method="magic_link")
)

client.reset_password_with_token(
    MagicLinkPasswordResetConfirmRequest(
        token="magic-link-token",
        new_password="new-password",
    )
)
```

### Company operations

```python
from userverse_python_client import UverseCompanyClient
from userverse_models.company.company import CompanyCreateModel

company_client = UverseCompanyClient(
    base_url="https://your-api-host/userverse",
    access_token=access_token,
)

company = company_client.create_company(
    CompanyCreateModel(name="Acme", email="info@acme.co.za")
)
```

### Roles and permissions

```python
from userverse_python_client import (
    UversePermissionManagementClient,
    UverseRoleManagementClient,
)
from userverse_models.company.roles import RoleCreateModel
from userverse_models.permissions import PermissionCreateModel

role_client = UverseRoleManagementClient(
    base_url="https://your-api-host/userverse",
    access_token=access_token,
)
permission_client = UversePermissionManagementClient(
    base_url="https://your-api-host/userverse",
    access_token=access_token,
)

role = role_client.create_role(
    RoleCreateModel(name="Auditor", description="Read audit records")
)
permission = permission_client.create_permission(
    PermissionCreateModel(
        name="audit.read",
        description="Read platform audit records",
    )
)
permission_client.assign_permission_to_role(role.data.id, permission.data.id)
```

## Userverse v0.7.0 response changes

Company membership records now expose a structured `role` object instead of a
`role_name` string. The role includes its id, name, description, and nested
permissions. Likewise, `UverseCompanyClient.get_user_companies()` now returns
`UserCompanyReadModel` records containing the requesting user's structured role.

Consumers migrating from an earlier release should replace access such as
`member.role_name` with `member.role.name`.

## Best Practices

- Log in once with `UverseUserClient`, then pass the access token into the company clients.
- Use the shared typed models from `softwareVerse-shared-python-utils` instead of raw dicts.
- Treat company ids and user ids as UUID strings when calling the SDK.
- Recreate or update the access token after refresh before making further JWT-protected calls.
- Handle `ClientErrorModel` explicitly so callers can inspect `status_code` and `payload.detail`.
- Pin released versions of both the client and shared models in production consumers.

## Demos

Runnable examples live in [`examples/`](examples):

- [`examples/user_demo_README.md`](examples/user_demo_README.md)
- [`examples/company_demo_README.md`](examples/company_demo_README.md)
- [`examples/company_user_management_demo_README.md`](examples/company_user_management_demo_README.md)
- [`examples/company_user_roles_demo_README.md`](examples/company_user_roles_demo_README.md)
- [`examples/rbac_demo_README.md`](examples/rbac_demo_README.md)

## Other Docs

- Multi-language SDK notes: [`docs/other-language-clients.md`](docs/other-language-clients.md)

## Development

Run tests:

```bash
uv run python -m pytest
```
