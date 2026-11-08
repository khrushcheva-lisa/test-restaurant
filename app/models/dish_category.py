from sqlmodel import SQLModel, Field

class Category(SQLModel, table=True):
    __tablename__ = "dishes_categories"

    category_dishes_id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str