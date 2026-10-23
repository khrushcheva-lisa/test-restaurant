from sqlmodel import SQLModel
from typing import Optional

class DishIngredientResponse(SQLModel):
    dish_ingredient_id : int
    ingredient_id : int
    dish_id : int
    quantity : int

    class Config:
        from_attributes = True

class DishIngredientCreate(SQLModel):
    ingredient_id: int
    dish_id: int
    quantity: int

class DishIngredientUpdate(SQLModel):
    quantity: Optional[int] = None