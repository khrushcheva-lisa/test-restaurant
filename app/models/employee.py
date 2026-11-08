from sqlmodel import SQLModel, Field
from datetime import date
from sqlalchemy import Column, Date

class Employee(SQLModel, table=True):
    __tablename__ = "employees"

    employee_id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    patronymic: str
    phone: str
    email: str
    position_id: str
    birth_date: date = Field(sa_column=Column("birthdate", Date))
    hire_date: date