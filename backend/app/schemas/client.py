from sqlmodel import SQLModel
from typing import Optional
from datetime import date


class ClientResponse(SQLModel):
    client_id : int
    first_name : str
    last_name : str
    patronymic : str
    email : str
    phone : str
    created_at : date

    class Config:
        from_attributes = True

class ClientCreate(SQLModel):
    first_name: str
    last_name: str
    patronymic: str
    email: str
    phone: str

class ClientUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None