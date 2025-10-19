from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UverseUserModel(BaseModel):
    id: int
    first_name: Optional[str] = Field(default="", description="First name of the user")
    last_name: Optional[str] = Field(default="", description="Last name of the user")
    email: EmailStr
    phone_number: Optional[str] = Field(
        default="", description="Phone number of the user"
    )
    is_superuser: bool = Field(
        False, description="Indicates if the user has superuser privileges"
    )
