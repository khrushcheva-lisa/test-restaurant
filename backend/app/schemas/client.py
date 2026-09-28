from pydantic import BaseModel
from datetime import date


class ClientResponse(BaseModel):
    client_id : int
    first_name : str
    last_name : str
    patronymic : str
    email : str
    phone : str
    created_at : date

    class Config:
        from_attributes = True

class ClientCreate(BaseModel):
    first_name: str
    last_name: str
    patronymic: str
    email: str
    phone: str