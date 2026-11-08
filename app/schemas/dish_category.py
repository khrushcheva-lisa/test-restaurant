from pydantic import BaseModel, ConfigDict, Field
from app.core.validation import NameValidation, DescriptionValidation

class CategoryCreate(NameValidation, DescriptionValidation):

    name: str = Field(min_length=2, max_length=80, description="Название категории", examples=["Супы"])
    description: str = Field(min_length=2, max_length=500, description="Описание категории", examples=["Жидкое блюдо, которое содержит не менее 50% жидкости и подается обычно в начале трапезы"])

class CategoryUpdate(NameValidation):
    name: str = Field(min_length=2, max_length=80, description="Название категории", examples=["Супы"])
    description: str = Field(min_length=2, max_length=500, description="Описание категории", examples=["Жидкое блюдо, которое содержит не менее 50% жидкости и подается обычно в начале трапезы"])

class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    category_dishes_id: int
    name: str
    description: str
