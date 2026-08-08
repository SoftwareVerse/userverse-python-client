from uuid import UUID

from sverse_generic_models.generic_pagination import PaginatedResponse
from sverse_generic_models.generic_response import GenericResponseModel
from userverse_models.company.roles import (
    RoleAssignCompaniesModel,
    RoleCreateModel,
    RoleQueryParamsModel,
    RoleReadModel,
    RoleUpdateModel,
)

from ..http_client_base import BaseClient


class UverseRoleManagementClient(BaseClient):
    """Manage global roles and their company assignments."""

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

    def create_role(
        self, role_data: RoleCreateModel
    ) -> GenericResponseModel[RoleReadModel]:
        response = self._request(
            "POST", "/roles", json=role_data.model_dump(exclude_none=True)
        )
        self._require_data(response, dict, "create role")
        return GenericResponseModel[RoleReadModel].model_validate(response)

    def get_roles(
        self, query_params: RoleQueryParamsModel | None = None
    ) -> GenericResponseModel[PaginatedResponse[RoleReadModel]]:
        query_params = query_params or RoleQueryParamsModel()
        response = self._request(
            "GET",
            "/roles",
            params=query_params.model_dump(exclude_none=True),
        )
        self._require_data(response, dict, "get roles")
        return GenericResponseModel[PaginatedResponse[RoleReadModel]].model_validate(
            response
        )

    def update_role(
        self, role_id: UUID | str, role_data: RoleUpdateModel
    ) -> GenericResponseModel[RoleReadModel]:
        response = self._request(
            "PATCH",
            f"/roles/{role_id}",
            json=role_data.model_dump(exclude_none=True),
        )
        self._require_data(response, dict, "update role")
        return GenericResponseModel[RoleReadModel].model_validate(response)

    def delete_role(self, role_id: UUID | str) -> GenericResponseModel[dict]:
        response = self._request("DELETE", f"/roles/{role_id}")
        self._require_data(response, dict, "delete role")
        return GenericResponseModel[dict].model_validate(response)

    def assign_role_to_companies(
        self,
        role_id: UUID | str,
        assignment: RoleAssignCompaniesModel,
    ) -> GenericResponseModel[dict]:
        response = self._request(
            "POST",
            f"/roles/{role_id}/companies",
            json=assignment.model_dump(exclude_none=True),
        )
        self._require_data(response, dict, "assign role to companies")
        return GenericResponseModel[dict].model_validate(response)

    def assign_role_to_company(
        self, company_id: UUID | str, role_id: UUID | str
    ) -> GenericResponseModel[RoleReadModel]:
        response = self._request("POST", f"/company/{company_id}/roles/{role_id}")
        self._require_data(response, dict, "assign role to company")
        return GenericResponseModel[RoleReadModel].model_validate(response)

    def unassign_role_from_company(
        self, company_id: UUID | str, role_id: UUID | str
    ) -> GenericResponseModel[dict]:
        response = self._request("DELETE", f"/company/{company_id}/roles/{role_id}")
        self._require_data(response, dict, "unassign role from company")
        return GenericResponseModel[dict].model_validate(response)
