import re
from pydantic import BaseModel, field_validator
from fastapi import HTTPException, status, Path
from datetime import date, datetime
from typing import Annotated

PositiveID = Annotated[
    int,
    Path(
        gt=0,
        description="Идентификатор должен быть положительным числом",
        examples=[1]
    )
]

class PersonNameValidation(BaseModel):
    @field_validator("first_name", "last_name", "patronymic", mode="before", check_fields=False)
    @classmethod
    def clean_person_name(cls, value):
        """Проверка имени, фамилии и отчества"""
        value = value.strip()

        if value is None or not isinstance(value, str) or not value.strip():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Поле не может быть пустым")

        value = value.strip()

        if len(value) < 2:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Должно быть не менее 2 символов")

        if len(value) > 50:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Должно быть не более 50 символов")

        if not re.fullmatch(r"[А-Яа-яЁёA-Za-z -]+", value):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Допустимы только буквы, пробел и дефис")

        return value

class NameValidation(BaseModel):

    @field_validator("name", mode="before", check_fields=False)
    @classmethod
    def clean_name(cls, value):
        """Проверка названия"""

        if value is None or not isinstance(value, str) or not value.strip():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Название не может быть пустым")

        value = value.strip()

        if len(value) < 2:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Название должно содержать не менее 2 символов")

        if len(value) > 100:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Название не должно превышать 100 символов")

        return value

class DescriptionValidation(BaseModel):

    @field_validator("description", mode="before", check_fields=False)
    @classmethod
    def clean_description(cls, value):
        """Проверка описания"""

        if value is None:
            return None

        if not isinstance(value, str):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Описание должно быть текстом")

        value = value.strip()

        if len(value) < 2:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Описание должно содержать не менее 2 символов")

        if len(value) > 500:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Описание не должно превышать 500 символов")

        return value

class ContactValidation(BaseModel):

    @field_validator("email", check_fields=False)
    @classmethod
    def clean_email(cls, value):
        """Проверка email"""
        if not value:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Email не может быть пустым")

        return value

    @field_validator("phone", mode="before", check_fields=False)
    @classmethod
    def clean_phone(cls, value):
        """Проверка номера телефона"""
        if not isinstance(value, str) or not value.strip():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Номер телефона не может быть пустым")

        value = value.strip()

        if not re.fullmatch(r"\+?[0-9()\- ]{7,20}", value):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=
                "Неверный формат номера телефона. Пример: +7 900 100 10 10")

        digits = re.sub(r"\D", "", value)

        if len(digits) != 11:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Номер телефона должен содержать 11 цифр")

        return value



class DateValidation(BaseModel):

    @field_validator("*", mode="before")
    @classmethod
    def validate_dates(cls, value):
        """Проверка даты на корректность и диапазон"""

        if value is None:
            return None

        if isinstance(value, datetime):
            value = value.date()

        elif isinstance(value, str):
            value = value.strip()

            if not value:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Дата не может быть пустой")

            try:
                value = date.fromisoformat(value)
            except ValueError:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Введите корректную дату в формате ГГГГ-ММ-ДД")

        if isinstance(value, date):
            if value > date.today() or value < date(1900, 1, 1):
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Дата не может быть в будущем или в прошлом более чем на 100 лет")

        return value

class DateTimeValidation(BaseModel):

    @field_validator("*", mode="before")
    @classmethod
    def validate_datetime(cls, value):
        """Проверка даты и времени на корректность и диапазон"""

        if value is None:
            return None

        if isinstance(value, str):
            value = value.strip()

            if not value:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Дата и время не могут быть пустыми")

            try:
                value = datetime.fromisoformat(value)
            except ValueError:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Введите корректные дату и время в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС")

        if isinstance(value, datetime):
            if value.tzinfo is not None:
                now = datetime.now(value.tzinfo)
            else:
                now = datetime.now()

            if value > now:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Дата и время не могут быть в будущем")

        return value

class PositiveIdValidation(BaseModel):

    @field_validator("*", mode="before")
    @classmethod
    def validate_ids(cls, value, info):

        if info.field_name == "id" or info.field_name.endswith("_id"):

            if value is None:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="ID не может быть пустым")

            if isinstance(value, bool) or not isinstance(value, int):
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="ID должен быть целым положительным числом")

            if value <= 0:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="ID должен быть больше нуля")

        return value

def translate_validation_error(error: dict) -> str:
    error_type = error.get("type")
    ctx = error.get("ctx") or {}

    custom_error = ctx.get("error")

    if custom_error:
        return str(custom_error)

    messages = {
        "missing": "Обязательное поле не заполнено",
        "string_too_short": (
            f"Слишком короткое значение. Минимум символов: "
            f"{ctx.get('min_length', '?')}"
        ),
        "string_too_long": (
            f"Слишком длинное значение. Максимум символов: "
            f"{ctx.get('max_length', '?')}"
        ),
        "greater_than": f"Значение должно быть больше {ctx.get('gt')}",
        "greater_than_equal": f"Значение должно быть не меньше {ctx.get('ge')}",
        "less_than": f"Значение должно быть меньше {ctx.get('lt')}",
        "less_than_equal": f"Значение должно быть не больше {ctx.get('le')}",
        "int_parsing": "Введите целое число",
        "float_parsing": "Введите корректное число",
        "int_type": "Значение должно быть целым числом",
        "float_type": "Значение должно быть числом",
        "string_type": "Значение должно быть текстом",
        "bool_parsing": "Введите корректное логическое значение",
        "string_pattern_mismatch": "Значение имеет неправильный формат",
        "json_invalid": "Некорректный формат JSON",
        "value_error": "Введено некорректное значение",
    }

    return messages.get(
        error_type,
        "Некорректно заполнено поле"
    )

