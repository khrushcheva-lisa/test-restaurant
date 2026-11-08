from sqlmodel import SQLModel, Field
from datetime import datetime

class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"

    order_item_id: int | None = Field(default=None, primary_key=True)
    order_id: int
    dish_id: int
    quantity: int
    price: float