from __future__ import annotations

import sys
from dataclasses import dataclass, field
from enum import Enum
from types import ModuleType
from typing import Any


@dataclass
class _DetailModel:
    message: str
    error: str | None = None


@dataclass
class _AppErrorResponseModel:
    detail: _DetailModel


class _GenericResponseModel:
    def __class_getitem__(cls, _item: Any) -> type["_GenericResponseModel"]:
        return cls

    @classmethod
    def model_validate(cls, payload: Any) -> Any:
        return payload


class _PaginatedResponse:
    def __class_getitem__(cls, _item: Any) -> type["_PaginatedResponse"]:
        return cls


@dataclass
class _ModelDumpMixin:
    def model_dump(self, exclude_none: bool = False) -> dict[str, Any]:
        data = dict(self.__dict__)
        if exclude_none:
            return {k: v for k, v in data.items() if v is not None}
        return data


@dataclass
class _UserLoginModel:
    email: str
    password: str


@dataclass
class _UserCreateModel:
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None


@dataclass
class _UserUpdateModel:
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    password: str | None = None


@dataclass
class _UserReadModel:
    id: str | None = None
    email: str | None = None


@dataclass
class _TokenResponseModel:
    token: str | None = None


@dataclass
class _RefreshTokenRequestModel(_ModelDumpMixin):
    refresh_token: str


@dataclass
class _TokenRevocationResponseModel:
    revoked: bool = True


@dataclass
class _PasswordResetRequest(_ModelDumpMixin):
    email: str
    method: str | None = None


@dataclass
class _MagicLinkPasswordResetConfirmRequest(_ModelDumpMixin):
    token: str
    new_password: str


@dataclass
class _UserQueryParams(_ModelDumpMixin):
    limit: int | None = None
    page: int | None = None
    role_name: str | None = None
    email: str | None = None


@dataclass
class _CompanyCreateModel(_ModelDumpMixin):
    name: str | None = None
    description: str | None = None
    industry: str | None = None
    phone_number: str | None = None
    email: str | None = None
    address: str | None = None


@dataclass
class _CompanyUpdateModel(_ModelDumpMixin):
    name: str | None = None
    description: str | None = None
    industry: str | None = None
    phone_number: str | None = None
    address: str | None = None


@dataclass
class _CompanyReadModel:
    id: str | None = None
    name: str | None = None


@dataclass
class _UserCompanyReadModel(_CompanyReadModel):
    role: object | None = None


@dataclass
class _CompanyQueryParamsModel(_ModelDumpMixin):
    limit: int | None = None
    page: int | None = None
    role_name: str | None = None
    name: str | None = None
    description: str | None = None
    industry: str | None = None
    email: str | None = None


@dataclass
class _CompanyUserAddModel(_ModelDumpMixin):
    email: str | None = None
    role: str | None = None


@dataclass
class _CompanyUserRoleUpdateModel(_ModelDumpMixin):
    role: str | None = None


@dataclass
class _CompanyUserReadModel:
    id: str | None = None
    email: str | None = None
    role: object | None = None


@dataclass
class _RoleCreateModel(_ModelDumpMixin):
    name: str | None = None
    description: str | None = None


@dataclass
class _RoleUpdateModel(_ModelDumpMixin):
    name: str | None = None
    description: str | None = None


@dataclass
class _RoleDeleteModel(_ModelDumpMixin):
    replacement_role_name: str | None = None
    role_name_to_delete: str | None = None


@dataclass
class _RoleReadModel:
    id: str | None = None
    name: str | None = None
    description: str | None = None
    permissions: list[object] = field(default_factory=list)


@dataclass
class _RoleAssignCompaniesModel(_ModelDumpMixin):
    company_ids: list[str] = field(default_factory=list)


@dataclass
class _RoleQueryParamsModel(_ModelDumpMixin):
    limit: int | None = None
    page: int | None = None
    name: str | None = None
    description: str | None = None


class _PermissionScope(str, Enum):
    GLOBAL = "global"
    COMPANY = "company"


@dataclass
class _PermissionCreateModel(_ModelDumpMixin):
    name: str
    description: str | None = None


@dataclass
class _PermissionUpdateModel(_ModelDumpMixin):
    name: str | None = None
    description: str | None = None


@dataclass
class _PermissionReadModel:
    id: str | None = None
    name: str | None = None
    description: str | None = None
    scope: _PermissionScope | None = None
    company_id: str | None = None


@dataclass
class _PermissionQueryParamsModel(_ModelDumpMixin):
    limit: int | None = None
    page: int | None = None
    name: str | None = None
    description: str | None = None


class _CompanyDefaultRoles(str, Enum):
    OWNER = "Owner: Full access"
    ADMINISTRATOR = "Administrator: Full access"
    VIEWER = "Viewer: Read-only access"

    @property
    def name_value(self) -> str:
        return self.value.split(":")[0].strip()


def _ensure_module(name: str) -> ModuleType:
    module = sys.modules.get(name)
    if module is None:
        module = ModuleType(name)
        module.__path__ = []
        sys.modules[name] = module
    return module


# Provide minimal stubs for external dependencies used by the client.
_ensure_module("sverse_generic_models")
app_error_module = _ensure_module("sverse_generic_models.app_error")
generic_response_module = _ensure_module("sverse_generic_models.generic_response")
generic_pagination_module = _ensure_module("sverse_generic_models.generic_pagination")
app_error_module.AppErrorResponseModel = _AppErrorResponseModel
app_error_module.DetailModel = _DetailModel
generic_response_module.GenericResponseModel = _GenericResponseModel
generic_pagination_module.PaginatedResponse = _PaginatedResponse

_ensure_module("userverse_models")
user_module = _ensure_module("userverse_models.user")
user_user_module = _ensure_module("userverse_models.user.user")
user_user_module.UserLoginModel = _UserLoginModel
user_user_module.UserUpdateModel = _UserUpdateModel
user_user_module.UserCreateModel = _UserCreateModel
user_user_module.UserReadModel = _UserReadModel
user_user_module.TokenResponseModel = _TokenResponseModel
user_user_module.RefreshTokenRequestModel = _RefreshTokenRequestModel
user_user_module.TokenRevocationResponseModel = _TokenRevocationResponseModel
user_user_module.UserQueryParams = _UserQueryParams
user_module.user = user_user_module
user_password_module = _ensure_module("userverse_models.user.password")
user_password_module.PasswordResetMethod = Enum(
    "PasswordResetMethod", {"OTP": "otp", "MAGIC_LINK": "magic_link"}, type=str
)
user_password_module.PasswordResetRequest = _PasswordResetRequest
user_password_module.MagicLinkPasswordResetConfirmRequest = (
    _MagicLinkPasswordResetConfirmRequest
)
user_module.password = user_password_module

company_module = _ensure_module("userverse_models.company")
company_company_module = _ensure_module("userverse_models.company.company")
company_company_module.CompanyCreateModel = _CompanyCreateModel
company_company_module.CompanyUpdateModel = _CompanyUpdateModel
company_company_module.CompanyReadModel = _CompanyReadModel
company_company_module.UserCompanyReadModel = _UserCompanyReadModel
company_company_module.CompanyQueryParamsModel = _CompanyQueryParamsModel
company_module.company = company_company_module
company_user_module = _ensure_module("userverse_models.company.user")
company_user_module.CompanyUserAddModel = _CompanyUserAddModel
company_user_module.CompanyUserReadModel = _CompanyUserReadModel
company_user_module.CompanyUserRoleUpdateModel = _CompanyUserRoleUpdateModel
company_module.user = company_user_module
company_roles_module = _ensure_module("userverse_models.company.roles")
company_roles_module.CompanyDefaultRoles = _CompanyDefaultRoles
company_roles_module.RoleCreateModel = _RoleCreateModel
company_roles_module.RoleUpdateModel = _RoleUpdateModel
company_roles_module.RoleDeleteModel = _RoleDeleteModel
company_roles_module.RoleReadModel = _RoleReadModel
company_roles_module.RoleAssignCompaniesModel = _RoleAssignCompaniesModel
company_roles_module.RoleQueryParamsModel = _RoleQueryParamsModel
company_module.roles = company_roles_module

permissions_module = _ensure_module("userverse_models.permissions")
permissions_module.PermissionScope = _PermissionScope
permissions_module.PermissionCreateModel = _PermissionCreateModel
permissions_module.PermissionUpdateModel = _PermissionUpdateModel
permissions_module.PermissionReadModel = _PermissionReadModel
permissions_module.PermissionQueryParamsModel = _PermissionQueryParamsModel
