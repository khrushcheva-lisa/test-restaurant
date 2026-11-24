from sqlmodel import SQLModel, Field

class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"

    order_item_id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.order_id")
    dish_id: int = Field(foreign_key="dishes.dish_id")
    quantity: int
    price: float
