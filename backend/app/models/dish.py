from sqlmodel import SQLModel, Field


class Dish(SQLModel, table=True):
    __tablename__ = "dishes"

    dish_id: int | None = Field(default=None, primary_key=True)
    category_dishes_id: int
    name: str
    description: str | None = None
    price: int
    weight_grams: int
    is_active: bool = True