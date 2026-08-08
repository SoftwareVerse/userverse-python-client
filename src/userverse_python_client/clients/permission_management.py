from uuid import UUID

from sverse_generic_models.generic_pagination import PaginatedResponse
from sverse_generic_models.generic_response import GenericResponseModel
from userverse_models.company.roles import RoleReadModel
from userverse_models.permissions import (
    PermissionCreateModel,
    PermissionQueryParamsModel,
    PermissionReadModel,
    PermissionUpdateModel,
)

from ..http_client_base import BaseClient


class UversePermissionManagementClient(BaseClient):
    """Manage global and company-scoped permissions."""

    @staticmethod
    def _require_data(response, expected_type: type, operation: str):
        if not response or "data" not in response:
            raise ValueError(f"Invalid response from {operation} endpoint")
        data = response.get("data")
        if not isinstance(data, expected_type):
            raise ValueError(
                f"Expected {operation} data to be {expected_type.__name__}, "
                f"got {type(data).__name__}"
            )
        return response

    def create_permission(
        self, permission_data: PermissionCreateModel
    ) -> GenericResponseModel[PermissionReadModel]:
        response = self._request(
            "POST",
            "/permissions",
            json=permission_data.model_dump(exclude_none=True),
        )
        self._require_data(response, dict, "create permission")
        return GenericResponseModel[PermissionReadModel].model_validate(response)

    def get_permissions(
        self, query_params: PermissionQueryParamsModel | None = None
    ) -> GenericResponseModel[PaginatedResponse[PermissionReadModel]]:
        query_params = query_params or PermissionQueryParamsModel()
        response = self._request(
            "GET",
            "/permissions",
            params=query_params.model_dump(exclude_none=True),
        )
        self._require_data(response, dict, "get permissions")
        return GenericResponseModel[
            PaginatedResponse[PermissionReadModel]
        ].model_validate(response)

    def update_permission(
        self,
        permission_id: UUID | str,
        permission_data: PermissionUpdateModel,
    ) -> GenericResponseModel[PermissionReadModel]:
        response = self._request(
            "PATCH",
            f"/permissions/{permission_id}",
            json=permission_data.model_dump(exclude_none=True),
        )
        self._require_data(response, dict, "update permission")
        return GenericResponseModel[PermissionReadModel].model_validate(response)

    def delete_permission(
        self, permission_id: UUID | str
    ) -> GenericResponseModel[dict]:
        response = self._request("DELETE", f"/permissions/{permission_id}")
        self._require_data(response, dict, "delete permission")
        return GenericResponseModel[dict].model_validate(response)

    def get_role_permissions(
        self, role_id: UUID | str
    ) -> GenericResponseModel[list[PermissionReadModel]]:
        response = self._request("GET", f"/roles/{role_id}/permissions")
        self._require_data(response, list, "get role permissions")
        return GenericResponseModel[list[PermissionReadModel]].model_validate(response)

    def assign_permission_to_role(
        self, role_id: UUID | str, permission_id: UUID | str
    ) -> GenericResponseModel[RoleReadModel]:
        response = self._request(
            "POST", f"/roles/{role_id}/permissions/{permission_id}"
        )
        self._require_data(response, dict, "assign permission to role")
        return GenericResponseModel[RoleReadModel].model_validate(response)

    def remove_permission_from_role(
        self, role_id: UUID | str, permission_id: UUID | str
    ) -> GenericResponseModel[RoleReadModel]:
        response = self._request(
            "DELETE", f"/roles/{role_id}/permissions/{permission_id}"
        )
        self._require_data(response, dict, "remove permission from role")
        return GenericResponseModel[RoleReadModel].model_validate(response)

    def create_company_permission(
        self,
        company_id: UUID | str,
        permission_data: PermissionCreateModel,
    ) -> GenericResponseModel[PermissionReadModel]:
        response = self._request(
            "POST",
            f"/company/{company_id}/permissions",
            json=permission_data.model_dump(exclude_none=True),
        )
        self._require_data(response, dict, "create company permission")
        return GenericResponseModel[PermissionReadModel].model_validate(response)

    def get_company_permissions(
        self,
        company_id: UUID | str,
        query_params: PermissionQueryParamsModel | None = None,
    ) -> GenericResponseModel[PaginatedResponse[PermissionReadModel]]:
        query_params = query_params or PermissionQueryParamsModel()
        response = self._request(
            "GET",
            f"/company/{company_id}/permissions",
            params=query_params.model_dump(exclude_none=True),
        )
        self._require_data(response, dict, "get company permissions")
        return GenericResponseModel[
            PaginatedResponse[PermissionReadModel]
        ].model_validate(response)

    def update_company_permission(
        self,
        company_id: UUID | str,
        permission_id: UUID | str,
        permission_data: PermissionUpdateModel,
    ) -> GenericResponseModel[PermissionReadModel]:
        response = self._request(
            "PATCH",
            f"/company/{company_id}/permissions/{permission_id}",
            json=permission_data.model_dump(exclude_none=True),
        )
        self._require_data(response, dict, "update company permission")
        return GenericResponseModel[PermissionReadModel].model_validate(response)

    def delete_company_permission(
        self, company_id: UUID | str, permission_id: UUID | str
    ) -> GenericResponseModel[dict]:
        response = self._request(
            "DELETE", f"/company/{company_id}/permissions/{permission_id}"
        )
        self._require_data(response, dict, "delete company permission")
        return GenericResponseModel[dict].model_validate(response)

    def get_company_role_permissions(
        self, company_id: UUID | str, role_id: UUID | str
    ) -> GenericResponseModel[list[PermissionReadModel]]:
        response = self._request(
            "GET", f"/company/{company_id}/roles/{role_id}/permissions"
        )
        self._require_data(response, list, "get company role permissions")
        return GenericResponseModel[list[PermissionReadModel]].model_validate(response)

    def assign_company_permission_to_role(
        self,
        company_id: UUID | str,
        role_id: UUID | str,
        permission_id: UUID | str,
    ) -> GenericResponseModel[RoleReadModel]:
        response = self._request(
            "POST",
            f"/company/{company_id}/roles/{role_id}/permissions/{permission_id}",
        )
        self._require_data(response, dict, "assign company permission to role")
        return GenericResponseModel[RoleReadModel].model_validate(response)

    def remove_company_permission_from_role(
        self,
        company_id: UUID | str,
        role_id: UUID | str,
        permission_id: UUID | str,
    ) -> GenericResponseModel[RoleReadModel]:
        response = self._request(
            "DELETE",
            f"/company/{company_id}/roles/{role_id}/permissions/{permission_id}",
        )
        self._require_data(response, dict, "remove company permission from role")
        return GenericResponseModel[RoleReadModel].model_validate(response)
