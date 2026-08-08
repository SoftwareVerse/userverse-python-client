import subprocess
import sys
import textwrap
from pathlib import Path


def test_shared_models_v014_supports_userverse_v070_contracts():
    """Validate the installed dependency without the unit-test module stubs."""
    script = textwrap.dedent("""
        from importlib.metadata import version

        from userverse_models.company.company import UserCompanyReadModel
        from userverse_models.company.roles import (
            RoleAssignCompaniesModel,
            RoleReadModel,
        )
        from userverse_models.company.user import CompanyUserReadModel
        from userverse_models.permissions import (
            PermissionCreateModel,
            PermissionReadModel,
        )
        from userverse_python_client import (
            UverseCompanyClient,
            UversePermissionManagementClient,
        )

        assert version("shared-models") == "0.1.14"

        permission = PermissionReadModel(
            id="550e8400-e29b-41d4-a716-446655440000",
            name="company.read",
            scope="global",
        )
        role = RoleReadModel(
            id="role-1",
            name="Owner",
            permissions=[permission],
        )
        company = UserCompanyReadModel(
            id="123e4567-e89b-12d3-a456-426614174000",
            email="info@example.com",
            role=role,
        )
        member = CompanyUserReadModel(
            id="d9428888-122b-11e1-b85c-61cd3cbb3210",
            email="member@example.com",
            role=role,
        )
        assignment = RoleAssignCompaniesModel(company_ids=[str(company.id)])

        assert company.role.permissions[0].name == "company.read"
        assert member.role.name == "Owner"
        assert assignment.company_ids == [str(company.id)]

        company_client = UverseCompanyClient("https://example.test", "token")
        company_client._request = lambda *_args, **_kwargs: {
            "message": "Companies found",
            "data": {
                "records": [company.model_dump(mode="json")],
                "pagination": {
                    "total_records": 1,
                    "limit": 10,
                    "current_page": 1,
                    "total_pages": 1,
                },
            },
        }
        companies = company_client.get_user_companies()
        assert companies.data.records[0].role.name == "Owner"

        permission_client = UversePermissionManagementClient(
            "https://example.test",
            "token",
        )
        permission_client._request = lambda *_args, **_kwargs: {
            "message": "Permission created",
            "data": permission.model_dump(mode="json"),
        }
        created = permission_client.create_permission(
            PermissionCreateModel(name="company.read")
        )
        assert created.data.scope.value == "global"
        """)

    result = subprocess.run(
        [str(Path(sys.prefix) / "bin" / "python"), "-c", script],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 0, result.stderr
