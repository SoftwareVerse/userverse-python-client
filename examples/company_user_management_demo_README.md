## Company User Management Demo

`examples/company_user_management_demo.py` demonstrates `UverseCompanyUserManagementClient`.

It covers:

- list company users
- add a user to a company by email
- update a company user's role
- remove a user from a company

## Run It

From the repo root:

```bash
uv run -m examples.company_user_management_demo --help
```

Use a local API:

```bash
USERVERSE_BASE_URL="http://localhost:8500/userverse" \
uv run -m examples.company_user_management_demo --help
```

## Common Flows

List company users:

```bash
USERVERSE_BASE_URL="http://localhost:8500/userverse" \
USER_EMAIL="you@example.com" USER_PASSWORD="secret" \
COMPANY_USER_COMPANY_ID="550e8400-e29b-41d4-a716-446655440000" \
uv run -m examples.company_user_management_demo --login --list-users
```

Add a user to a company:

```bash
USERVERSE_BASE_URL="http://localhost:8500/userverse" \
USER_EMAIL="you@example.com" USER_PASSWORD="secret" \
COMPANY_USER_COMPANY_ID="550e8400-e29b-41d4-a716-446655440000" \
COMPANY_USER_ADD_EMAIL="member@example.com" COMPANY_USER_ADD_ROLE="Viewer" \
uv run -m examples.company_user_management_demo --login --add-user
```

Update a member role:

```bash
USERVERSE_BASE_URL="http://localhost:8500/userverse" \
USER_EMAIL="you@example.com" USER_PASSWORD="secret" \
COMPANY_USER_COMPANY_ID="550e8400-e29b-41d4-a716-446655440000" \
COMPANY_USER_UPDATE_USER_ID="0d4f2f95-f7ca-4cb7-b6eb-ff4c7c43d9c6" \
COMPANY_USER_UPDATE_ROLE="Administrator" \
uv run -m examples.company_user_management_demo --login --update-user-role
```

Remove a user from a company:

```bash
USERVERSE_BASE_URL="http://localhost:8500/userverse" \
USER_EMAIL="you@example.com" USER_PASSWORD="secret" \
COMPANY_USER_COMPANY_ID="550e8400-e29b-41d4-a716-446655440000" \
COMPANY_USER_DELETE_USER_ID="0d4f2f95-f7ca-4cb7-b6eb-ff4c7c43d9c6" \
uv run -m examples.company_user_management_demo --login --delete-user
```

## Flags

- `--login`
- `--list-users`
- `--add-user`
- `--update-user-role`
- `--delete-user`
- `--all`

## Environment Variables

Shared:

- `USERVERSE_BASE_URL` optional
- `USER_EMAIL`
- `USER_PASSWORD`
- `COMPANY_USER_COMPANY_ID`

List filters:

- `COMPANY_USER_QUERY_LIMIT`
- `COMPANY_USER_QUERY_PAGE`
- `COMPANY_USER_QUERY_ROLE_NAME`
- `COMPANY_USER_QUERY_FIRST_NAME`
- `COMPANY_USER_QUERY_LAST_NAME`
- `COMPANY_USER_QUERY_EMAIL`

Add user:

- `COMPANY_USER_ADD_EMAIL`
- `COMPANY_USER_ADD_ROLE` optional, defaults to `Viewer`

Update role:

- `COMPANY_USER_UPDATE_USER_ID`
- `COMPANY_USER_UPDATE_ROLE`

Delete user:

- `COMPANY_USER_DELETE_USER_ID`

## Best Use

- Use email-based add flow when inviting or linking an existing user account to a company.
- Use role updates instead of remove-and-readd when only authorization changes.
- Treat both `COMPANY_USER_COMPANY_ID` and user ids as UUID strings.
