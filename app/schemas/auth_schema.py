from pydantic import BaseModel, Field

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str

class UserCreate(BaseModel):
    login: str = Field(min_length=3,max_length=50,pattern=r"^[A-Za-z0-9_.-]+$")
    password: str = Field(min_length=8,max_length=128)
    employee_id: int | None = Field(default=None,gt=0)
    role_id: int = Field(gt=0)

class UserRead(BaseModel):
    user_id: int
    login: str
    employee_id: int | None
    is_active: bool