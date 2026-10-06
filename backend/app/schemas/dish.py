from sqlmodel import SQLModel
from typing import Optional

class DishResponse(SQLModel):
    dish_id : int
    category_dishes_id : int
    name : str
    description : str
    price : int
    weight_grams : int
    is_active : bool

    class Config:
        from_attributes = True

class DishCreate(SQLModel):
    category_dishes_id : int
    name: str
    description: str
    price: int
    weight_grams : int
    is_active : bool = True

class DishUpdate(SQLModel):
    category_dishes_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    weight_grams: Optional[int] = None
    is_active: Optional[bool] = None