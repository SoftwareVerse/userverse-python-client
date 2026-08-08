from userverse_models.company.roles import (
    RoleAssignCompaniesModel,
    RoleCreateModel,
)
from userverse_models.permissions import PermissionCreateModel
from userverse_python_client import (
    UversePermissionManagementClient,
    UversePlatformRoleManagementClient,
    UverseRoleManagementClient,
    UverseUserClient,
)


def run_rbac_demo(
    base_url: str,
    access_token: str,
    company_id: str,
    user_id: str,
) -> None:
    role_client = UverseRoleManagementClient(base_url, access_token)
    permission_client = UversePermissionManagementClient(base_url, access_token)
    platform_role_client = UversePlatformRoleManagementClient(base_url, access_token)
    user_client = UverseUserClient(base_url, access_token)

    role_response = role_client.create_role(
        RoleCreateModel(
            name="Auditor",
            description="Read audit records",
        )
    )
    permission_response = permission_client.create_permission(
        PermissionCreateModel(
            name="audit.read",
            description="Read platform audit records",
        )
    )

    role_id = role_response.data.id
    permission_id = permission_response.data.id

    permission_client.assign_permission_to_role(role_id, permission_id)
    role_client.assign_role_to_companies(
        role_id,
        RoleAssignCompaniesModel(company_ids=[company_id]),
    )
    platform_role_client.assign_role_to_user(user_id, role_id)

    effective_permissions = user_client.get_user_permissions()
    for permission in effective_permissions.data or []:
        print(permission.name, permission.scope)
