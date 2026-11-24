from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class EmployeeCreate(BaseModel):
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    patronymic: str = Field(min_length=2, max_length=50)
    email: EmailStr
    phone: str = Field(pattern=r"^\+?[0-9()\- ]{7,20}$")
    position_id: int = Field(gt=0)
    birth_date: date
    hire_date: date

class EmployeeUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=2, max_length=50)
    last_name: str | None = Field(default=None, min_length=2, max_length=50)
    patronymic: str | None = Field(default=None, min_length=2, max_length=50)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, pattern=r"^\+?[0-9()\- ]{7,20}$")
    position_id: int | None = Field(default=None, gt=0)
    birth_date: date | None = None
    hire_date: date | None = None

class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    employee_id: int
    first_name: str
    last_name: str
    patronymic: str
    phone: str
    email: EmailStr
    position_id: int
    birth_date: date
    hire_date: date
