from sqlmodel import SQLModel, Field
from datetime import datetime

class Order(SQLModel, table=True):
    __tablename__ = "orders"

    order_id: int | None = Field(default=None, primary_key=True)
    client_id: int
    waiter_id: int
    total_amount: int
    status_id: int
    created_at: datetime
    completed_at: datetime | None = None