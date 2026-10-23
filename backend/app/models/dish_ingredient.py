from sqlmodel import Field, SQLModel


class DishIngredient(SQLModel, table=True):
    __tablename__ = "dishes_ingredients"

    dish_id: int = Field(foreign_key="dishes.dish_id", primary_key=True)
    ingredient_id: int = Field(foreign_key="ingredients.ingredient_id", primary_key=True)
