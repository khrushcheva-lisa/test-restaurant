from sqlmodel import SQLModel, Field
from datetime import date

class Client(SQLModel, table=True):
    __tablename__ = "clients"

    client_id: int | None = Field(default=None, primary_key=True)
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    patronymic: str = Field(min_length=2, max_length=50)
    email: str
    phone: str
    created_at: date