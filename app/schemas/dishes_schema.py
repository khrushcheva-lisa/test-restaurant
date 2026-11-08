from pydantic import BaseModel, ConfigDict, Field
from app.core.validation import NameValidation, DescriptionValidation

class DishCreate(NameValidation, DescriptionValidation):

    category_dishes_id: int = Field(gt=0, description="ID категории блюд", examples=[1, 2, 3])
    name: str = Field(min_length=2, max_length=100, description="Название блюда", examples=["Борщ"])
    description: str | None = Field(default=None, max_length=1000, description="Описание блюда", examples=["Традиционный украинский суп"])
    price: int = Field(gt=0, description="Цена блюда", examples=[100, 200, 300])
    weight_grams: int = Field(gt=0, le=10000, description="Вес блюда в граммах", examples=[500, 1000, 1500])


class DishUpdate(NameValidation, DescriptionValidation):
    category_dishes_id: int | None = Field(default=None, gt=0, description="ID категории блюд", examples=[1, 2, 3])
    name: str | None = Field(default=None, min_length=2, max_length=100, description="Название блюда", examples=["Борщ"])
    description: str | None = Field(default=None, max_length=1000, description="Описание блюда", examples=["Традиционный украинский суп"])
    price: int | None = Field(default=None, gt=0, description="Цена блюда", examples=[100, 200, 300])
    weight_grams: int | None = Field(default=None, gt=0, le=10000, description="Вес блюда в граммах", examples=[500, 1000, 1500])
    is_active: bool | None = Field(default=None, description="Статус блюда", examples=[True, False])


class DishResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    dish_id: int
    category_dishes_id: int
    name: str
    description: str | None
    price: int
    weight_grams: int
    is_active: bool
