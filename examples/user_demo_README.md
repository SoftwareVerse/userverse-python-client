## User Demo

`examples/user_demo.py` demonstrates the current `UverseUserClient` surface.

It covers:

- login
- create user
- refresh token
- revoke refresh token
- get current user
- update current user
- resend verification email
- verify user
- request password reset
- reset password by OTP
- reset password by magic-link token
- delete current user

## Run It

From the repo root:

```bash
uv run -m examples.user_demo --help
```

Override the API host if needed:

```bash
USERVERSE_BASE_URL="http://localhost:8500/userverse" uv run -m examples.user_demo --help
```

## Common Flows

Login and fetch the current user:

```bash
USERVERSE_BASE_URL="http://localhost:8500/userverse" \
USER_EMAIL="you@example.com" USER_PASSWORD="secret" \
uv run -m examples.user_demo --login --get-user
```

Create a user:

```bash
USERVERSE_BASE_URL="http://localhost:8500/userverse" \
NEW_USER_EMAIL="new@example.com" NEW_USER_PASSWORD="secret" \
NEW_USER_FIRST_NAME="New" NEW_USER_LAST_NAME="User" \
uv run -m examples.user_demo --create-user
```

Refresh tokens:

```bash
USERVERSE_BASE_URL="http://localhost:8500/userverse" \
USER_REFRESH_TOKEN="refresh-token" \
uv run -m examples.user_demo --refresh-token
```

Request OTP password reset:

```bash
USERVERSE_BASE_URL="http://localhost:8500/userverse" \
RESET_EMAIL="you@example.com" RESET_METHOD="otp" \
uv run -m examples.user_demo --request-password-reset
```

Complete OTP password reset:

```bash
USERVERSE_BASE_URL="http://localhost:8500/userverse" \
RESET_EMAIL="you@example.com" RESET_NEW_PASSWORD="new-secret" RESET_OTP="123456" \
uv run -m examples.user_demo --reset-password-otp
```

Complete magic-link password reset:

```bash
USERVERSE_BASE_URL="http://localhost:8500/userverse" \
RESET_TOKEN="token-from-email" RESET_NEW_PASSWORD="new-secret" \
uv run -m examples.user_demo --reset-password-token
```

## Flags

- `--login`
- `--create-user`
- `--refresh-token`
- `--revoke-token`
- `--get-user`
- `--update-user`
- `--resend-verification`
- `--verify-user`
- `--request-password-reset`
- `--reset-password-otp`
- `--reset-password-token`
- `--delete-user`
- `--all`

## Environment Variables

Shared:

- `USERVERSE_BASE_URL` optional, defaults to `https://apps.oxillium-api.co.za/userverse`

Login:

- `USER_EMAIL`
- `USER_PASSWORD`

Create user:

- `NEW_USER_EMAIL`
- `NEW_USER_PASSWORD`
- `NEW_USER_FIRST_NAME` optional
- `NEW_USER_LAST_NAME` optional
- `NEW_USER_PHONE_NUMBER` optional

Refresh/revoke:

- `USER_REFRESH_TOKEN`

Update user:

- `UPDATE_FIRST_NAME` optional
- `UPDATE_LAST_NAME` optional
- `UPDATE_PHONE_NUMBER` optional
- `UPDATE_PASSWORD` optional

Verification:

- `VERIFY_EMAIL` for resend
- `VERIFY_TOKEN` for verify

Password reset:

- `RESET_EMAIL`
- `RESET_METHOD` optional, defaults to `otp`
- `RESET_NEW_PASSWORD`
- `RESET_OTP` for OTP flow
- `RESET_TOKEN` for magic-link flow

## Best Use

- Use `--login` before JWT-protected actions such as `--get-user`, `--update-user`, and `--delete-user`.
- Use `--refresh-token` when you already have a refresh token and need a new access token.
- Use `--revoke-token` when ending a session family, for example on logout from a trusted backend flow.
- Use OTP reset when your integration already handles code entry.
- Use magic-link reset when your UI flow is email-link driven.
