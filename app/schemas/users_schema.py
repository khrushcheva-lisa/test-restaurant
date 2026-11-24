from datetime import date
from pydantic import BaseModel, ConfigDict, Field

class UserCreate(BaseModel):
    login: str = Field(min_length=3, max_length=33, pattern=r"^[A-Za-z0-9_.-]+$")
    password: str = Field(min_length=8, max_length=128)
    employee_id: int | None = Field(default=None, gt=0)
    role_id: int = Field(gt=0)

class UserUpdate(BaseModel):
    login: str | None = Field(default=None, min_length=3, max_length=33, pattern=r"^[A-Za-z0-9_.-]+$")
    password: str | None = Field(default=None, min_length=8, max_length=128)
    employee_id: int | None = Field(default=None, gt=0)
    is_active: bool | None = None

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    employee_id: int | None
    login: str
    is_active: bool
    created_at: date
    last_login_at: date | None
