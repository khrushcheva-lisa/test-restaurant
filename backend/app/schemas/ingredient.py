from sqlmodel import SQLModel
from typing import Optional

class IngredientResponse(SQLModel):
    ingredient_id : int
    name : str

    class Config:
        from_attributes = True

class IngredientCreate(SQLModel):
    name: str

class IngredientUpdate(SQLModel):
    name: Optional[str] = None