from sqlmodel import SQLModel, Field

class Ingredient(SQLModel, table=True):
    __tablename__ = "ingredients"

    ingredient_id: int | None = Field(default=None, primary_key=True)
    name: str