Examples

This folder contains runnable demos for the client library. The main script is
`user_demo.py`, which shows how to call the user endpoints with the
`UverseUserClient`.

Running the demo

The script is designed to turn features on/off using flags. Each action pulls
credentials or tokens from environment variables. If a required variable is
missing, that action is skipped with a message.

Run from the repo root:

```
uv run -m examples.user_demo --help
```

Common usage

Login and get the current user:

```
USER_EMAIL="you@example.com" USER_PASSWORD="secret" \
uv run -m examples.user_demo --login --get-user
```

Create a user (uses Basic Auth for the new user):

```
NEW_USER_EMAIL="new@example.com" NEW_USER_PASSWORD="secret" \
NEW_USER_FIRST_NAME="New" NEW_USER_LAST_NAME="User" \
uv run -m examples.user_demo --create-user
```

Update current user (requires login):

```
USER_EMAIL="you@example.com" USER_PASSWORD="secret" \
UPDATE_FIRST_NAME="Updated" UPDATE_LAST_NAME="Name" \
uv run -m examples.user_demo --login --update-user
```

Available flags

- --login
- --create-user
- --get-user
- --update-user
- --resend-verification
- --verify-user
- --request-password-reset
- --reset-password
- --all

Environment variables

Login:
- USER_EMAIL
- USER_PASSWORD

Create user:
- NEW_USER_EMAIL
- NEW_USER_PASSWORD
- NEW_USER_FIRST_NAME (optional)
- NEW_USER_LAST_NAME (optional)
- NEW_USER_PHONE_NUMBER (optional)

Update user:
- UPDATE_FIRST_NAME (optional)
- UPDATE_LAST_NAME (optional)
- UPDATE_PHONE_NUMBER (optional)
- UPDATE_PASSWORD (optional)

Verify email:
- VERIFY_TOKEN

Password reset request:
- RESET_EMAIL

Password reset confirm:
- RESET_EMAIL
- RESET_NEW_PASSWORD
- RESET_OTP
