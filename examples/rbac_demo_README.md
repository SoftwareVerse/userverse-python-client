# Userverse v0.7.0 RBAC demo

`rbac_demo.py` demonstrates the typed role and permission clients introduced for
Userverse v0.7.0. The access token used for global role and permission management
must belong to a Userverse superuser.

The flow:

1. Creates a global role and permission.
2. Assigns the permission to the role.
3. Makes the role available to a company.
4. Assigns the platform role to a user.
5. Reads the current user's effective platform permissions.

Import and call `run_rbac_demo()` with the API base URL, a suitable access token,
and existing company and user ids. The example intentionally leaves authentication
and cleanup to the calling application.
