from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.core.validation import NameValidation

class IngredientCreate(NameValidation):

    name: str = Field(min_length=2, max_length=100, description="Название ингредиента", examples=["Картофель"])

class IngredientUpdate(NameValidation):
    name: str | None = Field(default=None, min_length=2, max_length=100, description="Название ингредиента", examples=["Картофель"])

class IngredientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    ingredient_id: int
    name: str
