from sqlmodel import SQLModel, Field
from datetime import date

class User(SQLModel, table=True):
    __tablename__ = "users"

    user_id: int | None = Field(default=None, primary_key=True)
    employee_id: int | None = Field(default=None, foreign_key="employees.employee_id")
    login: str
    password_hash: str
    is_active: bool = Field(default=True)
    created_at: date = Field(default_factory=date.today)
    last_login_at: date | None = Field(default=None)