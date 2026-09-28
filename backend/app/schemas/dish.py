from pydantic import BaseModel


class DishResponse(BaseModel):
    dish_id : int
    category_dishes_id : int
    name : str
    description : str
    price : int
    weight_grams : int
    is_active : bool

    class Config:
        from_attributes = True