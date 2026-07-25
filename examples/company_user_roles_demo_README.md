## Company Role Management Demo

`examples/company_user_roles_demo.py` demonstrates `UverseCompanyUserRolesManagement`.

It covers:

- list company roles
- create a role
- update a role
- delete a role with replacement
- print built-in default roles

## Run It

From the repo root:

```bash
uv run -m examples.company_user_roles_demo --help
```

Use a local API:

```bash
USERVERSE_BASE_URL="http://localhost:8500/userverse" \
uv run -m examples.company_user_roles_demo --help
```

## Common Flows

List roles:

```bash
USERVERSE_BASE_URL="http://localhost:8500/userverse" \
USER_EMAIL="you@example.com" USER_PASSWORD="secret" \
COMPANY_ROLE_COMPANY_ID="550e8400-e29b-41d4-a716-446655440000" \
uv run -m examples.company_user_roles_demo --login --list-roles
```

Create a role:

```bash
USERVERSE_BASE_URL="http://localhost:8500/userverse" \
USER_EMAIL="you@example.com" USER_PASSWORD="secret" \
COMPANY_ROLE_COMPANY_ID="550e8400-e29b-41d4-a716-446655440000" \
COMPANY_ROLE_CREATE_NAME="Supervisor" \
COMPANY_ROLE_CREATE_DESCRIPTION="Can approve requests" \
uv run -m examples.company_user_roles_demo --login --create-role
```

Update a role:

```bash
USERVERSE_BASE_URL="http://localhost:8500/userverse" \
USER_EMAIL="you@example.com" USER_PASSWORD="secret" \
COMPANY_ROLE_COMPANY_ID="550e8400-e29b-41d4-a716-446655440000" \
COMPANY_ROLE_UPDATE_ROLE_NAME="Supervisor" \
COMPANY_ROLE_UPDATE_DESCRIPTION="Approves and audits" \
uv run -m examples.company_user_roles_demo --login --update-role
```

Delete a role:

```bash
USERVERSE_BASE_URL="http://localhost:8500/userverse" \
USER_EMAIL="you@example.com" USER_PASSWORD="secret" \
COMPANY_ROLE_COMPANY_ID="550e8400-e29b-41d4-a716-446655440000" \
COMPANY_ROLE_DELETE_NAME="Seasonal Contractor" \
COMPANY_ROLE_DELETE_REPLACEMENT="Viewer" \
uv run -m examples.company_user_roles_demo --login --delete-role
```

Print built-in roles:

```bash
uv run -m examples.company_user_roles_demo --default-roles
```

## Flags

- `--login`
- `--list-roles`
- `--create-role`
- `--update-role`
- `--delete-role`
- `--default-roles`
- `--all`

## Environment Variables

Shared:

- `USERVERSE_BASE_URL` optional
- `USER_EMAIL`
- `USER_PASSWORD`
- `COMPANY_ROLE_COMPANY_ID`

List filters:

- `COMPANY_ROLE_QUERY_LIMIT`
- `COMPANY_ROLE_QUERY_PAGE`
- `COMPANY_ROLE_QUERY_NAME`
- `COMPANY_ROLE_QUERY_DESCRIPTION`

Create:

- `COMPANY_ROLE_CREATE_NAME`
- `COMPANY_ROLE_CREATE_DESCRIPTION` optional

Update:

- `COMPANY_ROLE_UPDATE_ROLE_NAME`
- `COMPANY_ROLE_UPDATE_NAME` optional
- `COMPANY_ROLE_UPDATE_DESCRIPTION` optional

Delete:

- `COMPANY_ROLE_DELETE_NAME`
- `COMPANY_ROLE_DELETE_REPLACEMENT`

## Best Use

- Use `--default-roles` to discover the baseline role names before creating custom ones.
- Keep custom role names stable and update descriptions first when changing semantics.
- Deleting a role requires a safe replacement role for existing members; plan that reassignment deliberately.
