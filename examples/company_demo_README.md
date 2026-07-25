## Company Demo

`examples/company_demo.py` demonstrates `UverseCompanyClient`.

It covers:

- list authenticated user companies
- get a company by UUID
- get a company by email
- create a company
- update a company

## Run It

From the repo root:

```bash
uv run -m examples.company_demo --help
```

Use a local API service:

```bash
USERVERSE_BASE_URL="http://localhost:8500/userverse" uv run -m examples.company_demo --help
```

## Common Flows

Login and list companies:

```bash
USERVERSE_BASE_URL="http://localhost:8500/userverse" \
USER_EMAIL="you@example.com" USER_PASSWORD="secret" \
uv run -m examples.company_demo --login --list-companies
```

Lookup by company UUID:

```bash
USERVERSE_BASE_URL="http://localhost:8500/userverse" \
USER_EMAIL="you@example.com" USER_PASSWORD="secret" \
uv run -m examples.company_demo --login --get-company-by-id 550e8400-e29b-41d4-a716-446655440000
```

Create a company:

```bash
USERVERSE_BASE_URL="http://localhost:8500/userverse" \
USER_EMAIL="you@example.com" USER_PASSWORD="secret" \
COMPANY_CREATE_NAME="Acme Corp" COMPANY_CREATE_EMAIL="info@acme.co.za" \
COMPANY_CREATE_ADDRESS_CITY="Cape Town" COMPANY_CREATE_ADDRESS_COUNTRY="South Africa" \
uv run -m examples.company_demo --login --create-company
```

Update a company:

```bash
USERVERSE_BASE_URL="http://localhost:8500/userverse" \
USER_EMAIL="you@example.com" USER_PASSWORD="secret" \
COMPANY_UPDATE_ID="550e8400-e29b-41d4-a716-446655440000" \
COMPANY_UPDATE_DESCRIPTION="Updated description" \
uv run -m examples.company_demo --login --update-company
```

## Flags

- `--login`
- `--list-companies`
- `--get-company-by-id`
- `--get-company-by-email`
- `--create-company`
- `--update-company`
- `--all`

## Environment Variables

Shared:

- `USERVERSE_BASE_URL` optional
- `USER_EMAIL`
- `USER_PASSWORD`

List filters:

- `COMPANY_QUERY_LIMIT`
- `COMPANY_QUERY_PAGE`
- `COMPANY_QUERY_ROLE_NAME`
- `COMPANY_QUERY_NAME`
- `COMPANY_QUERY_DESCRIPTION`
- `COMPANY_QUERY_INDUSTRY`
- `COMPANY_QUERY_EMAIL`

Lookup:

- `COMPANY_LOOKUP_ID`
- `COMPANY_LOOKUP_EMAIL`

Create:

- `COMPANY_CREATE_NAME`
- `COMPANY_CREATE_EMAIL`
- `COMPANY_CREATE_DESCRIPTION` optional
- `COMPANY_CREATE_INDUSTRY` optional
- `COMPANY_CREATE_PHONE_NUMBER` optional
- `COMPANY_CREATE_ADDRESS_JSON` optional JSON object
- `COMPANY_CREATE_ADDRESS_STREET` optional
- `COMPANY_CREATE_ADDRESS_CITY` optional
- `COMPANY_CREATE_ADDRESS_STATE` optional
- `COMPANY_CREATE_ADDRESS_POSTAL_CODE` optional
- `COMPANY_CREATE_ADDRESS_COUNTRY` optional

Update:

- `COMPANY_UPDATE_ID`
- `COMPANY_UPDATE_NAME` optional
- `COMPANY_UPDATE_DESCRIPTION` optional
- `COMPANY_UPDATE_INDUSTRY` optional
- `COMPANY_UPDATE_PHONE_NUMBER` optional
- `COMPANY_UPDATE_ADDRESS_JSON` optional JSON object
- `COMPANY_UPDATE_ADDRESS_STREET` optional
- `COMPANY_UPDATE_ADDRESS_CITY` optional
- `COMPANY_UPDATE_ADDRESS_STATE` optional
- `COMPANY_UPDATE_ADDRESS_POSTAL_CODE` optional
- `COMPANY_UPDATE_ADDRESS_COUNTRY` optional

## Best Use

- Log in once and reuse the returned access token for all company flows.
- Treat company ids as UUID strings, not integers.
- Prefer address field env vars or `*_ADDRESS_JSON` over flat string addresses.
- Use list filtering when your integration needs lightweight search without an extra lookup round-trip.
