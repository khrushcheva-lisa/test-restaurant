from sqlmodel import SQLModel, Field
from datetime import date

class Menu(SQLModel, table=True):
    __tablename__ = "menu"

    menu_id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    valid_from: date
    valid_to: date
    is_active: bool = Field(default=True)
    created_at: date = Field(default=date.today())