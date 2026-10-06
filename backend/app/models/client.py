from sqlmodel import SQLModel, Field
from datetime import date

class Client(SQLModel, table=True):
    __tablename__ = "clients"

    client_id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    patronymic: str
    email: str
    phone: str
    created_at: date