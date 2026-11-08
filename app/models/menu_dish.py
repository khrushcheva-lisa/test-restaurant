from sqlmodel import SQLModel, Field

class MenuDish(SQLModel, table=True):
    __tablename__ = "menu_dishes"

    menu_dish_id: int | None = Field(default=None, primary_key=True)
    menu_id: int | None = Field(default=None, primary_key=True)
    dish_id: int | None = Field(default=None, primary_key=True)