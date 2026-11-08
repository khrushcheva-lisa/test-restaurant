from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.core.validation import PersonNameValidation, ContactValidation, DateValidation


class ClientCreate(PersonNameValidation, ContactValidation, DateValidation):

    last_name: str = Field(min_length=2, max_length=50, description="Фамилия", examples=["Иванов"])
    first_name: str = Field(min_length=2, max_length=50, description="Имя", examples=["Иван"])
    patronymic: str = Field(min_length=2, max_length=50, description="Отчество", examples=["Иванович"])
    email: EmailStr
    phone: str = Field(pattern=r"^\+?[0-9()\- ]{7,20}$", description="Номер телефона", examples=["+7 900 100 10 10"])
    created_at: date = Field(default_factory=date.today)


class ClientUpdate(PersonNameValidation, ContactValidation):
    last_name: str | None = Field(default=None, min_length=2, max_length=50, description="Фамилия", examples=["Иванов"])
    first_name: str | None = Field(default=None, min_length=2, max_length=50, description="Имя", examples=["Иван"])
    patronymic: str | None = Field(default=None, min_length=2, max_length=50, description="Отчество", examples=["Иванович"])
    email: EmailStr | None = None
    phone: str | None = Field(default=None, pattern=r"^\+?[0-9()\- ]{7,20}$", description="Номер телефона", examples=["+7 900 100 10 10"])


class ClientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    client_id: int
    first_name: str
    last_name: str
    patronymic: str
    email: EmailStr
    phone: str
    created_at: date
