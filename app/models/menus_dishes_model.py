from sqlmodel import SQLModel, Field

class MenuDish(SQLModel, table=True):
    __tablename__ = "menu_dishes"

    menu_dish_id: int | None = Field(default=None, primary_key=True)
    menu_id: int = Field(foreign_key="menu.menu_id")
    dish_id: int = Field(foreign_key="dishes.dish_id")
