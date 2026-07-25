from uuid import UUID

from sverse_generic_models.generic_response import GenericResponseModel
from sverse_generic_models.generic_pagination import PaginatedResponse
from userverse_models.user.user import UserQueryParams
from userverse_models.company.user import (
    CompanyUserReadModel,
    CompanyUserAddModel,
    CompanyUserRoleUpdateModel,
)

from ..http_client_base import BaseClient


class UverseCompanyUserManagementClient(BaseClient):
    def __init__(self, base_url, access_token, timeout=30):
        super().__init__(base_url, access_token, timeout)

    def add_user_to_company(
        self, company_id: UUID | str, user_data: CompanyUserAddModel
    ) -> GenericResponseModel[CompanyUserReadModel]:
        """Create a new company user membership for the provided company."""

        payload = user_data.model_dump(exclude_none=True)

        response = self._request(
            "POST",
            f"/company/{company_id}/users",
            json=payload,
        )

        if not response or "data" not in response:
            raise ValueError("Invalid response from add user to company endpoint")

        data = response.get("data", {})
        if not isinstance(data, dict):
            raise ValueError(
                f"Expected company user data to be a dict, got {type(data)}"
            )

        return GenericResponseModel[CompanyUserReadModel].model_validate(response)

    def delete_user_from_company(
        self, company_id: UUID | str, user_id: UUID | str
    ) -> GenericResponseModel[CompanyUserReadModel]:
        """Remove a user from the specified company."""

        response = self._request(
            "DELETE",
            f"/company/{company_id}/user/{user_id}",
        )

        if response is None or "data" not in response:
            raise ValueError("Invalid response from delete company user endpoint")

        data = response.get("data", {})
        if not isinstance(data, dict):
            raise ValueError(
                f"Expected company user data to be a dict, got {type(data)}"
            )

        return GenericResponseModel[CompanyUserReadModel].model_validate(response)

    def update_user_role(
        self,
        company_id: UUID | str,
        user_id: UUID | str,
        user_role: CompanyUserRoleUpdateModel,
    ) -> GenericResponseModel[CompanyUserReadModel]:
        """Update a company user's role."""
        payload = user_role.model_dump(exclude_none=True)

        response = self._request(
            "PATCH",
            f"/company/{company_id}/user/{user_id}",
            json=payload,
        )

        if not response or "data" not in response:
            raise ValueError("Invalid response from update company user role endpoint")

        data = response.get("data", {})
        if not isinstance(data, dict):
            raise ValueError(
                f"Expected company user data to be a dict, got {type(data)}"
            )

        return GenericResponseModel[CompanyUserReadModel].model_validate(response)

    def list_company_users(
        self,
        company_id: UUID | str,
        query_params: UserQueryParams = UserQueryParams(),
    ) -> GenericResponseModel[PaginatedResponse[CompanyUserReadModel]]:
        """Fetch paginated company users for the provided company id."""

        params = query_params.model_dump(exclude_none=True)

        response = self._request(
            "GET",
            f"/company/{company_id}/users",
            params=params,
        )

        if not response or "data" not in response:
            raise ValueError("Invalid response from list company users endpoint")

        data = response.get("data", {})
        if not isinstance(data, dict):
            raise ValueError(
                f"Expected company user pagination data to be a dict, got {type(data)}"
            )

        return GenericResponseModel[
            PaginatedResponse[CompanyUserReadModel]
        ].model_validate(response)
