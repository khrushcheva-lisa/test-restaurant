from sqlmodel import SQLModel, Field
from datetime import date

class Employee(SQLModel, table=True):
    __tablename__ = "employees"

    employee_id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    patronymic: str
    phone: str
    email: str
    position_id: str
    birth_date: date
    hire_date: date