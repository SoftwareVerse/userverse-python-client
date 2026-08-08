from uuid import UUID

from sverse_generic_models.generic_response import GenericResponseModel
from userverse_models.company.roles import RoleReadModel

from ..http_client_base import BaseClient


class UversePlatformRoleManagementClient(BaseClient):
    """Manage platform roles assigned directly to users."""

    @staticmethod
    def _validate_response(response, operation: str):
        if not response or "data" not in response:
            raise ValueError(f"Invalid response from {operation} endpoint")
        if not isinstance(response.get("data"), list):
            raise ValueError(f"Expected {operation} data to be a list")
        return GenericResponseModel[list[RoleReadModel]].model_validate(response)

    def get_user_roles(
        self, user_id: UUID | str
    ) -> GenericResponseModel[list[RoleReadModel]]:
        response = self._request("GET", f"/users/{user_id}/roles")
        return self._validate_response(response, "get user roles")

    def assign_role_to_user(
        self, user_id: UUID | str, role_id: UUID | str
    ) -> GenericResponseModel[list[RoleReadModel]]:
        response = self._request("POST", f"/users/{user_id}/roles/{role_id}")
        return self._validate_response(response, "assign role to user")

    def remove_role_from_user(
        self, user_id: UUID | str, role_id: UUID | str
    ) -> GenericResponseModel[list[RoleReadModel]]:
        response = self._request("DELETE", f"/users/{user_id}/roles/{role_id}")
        return self._validate_response(response, "remove role from user")
