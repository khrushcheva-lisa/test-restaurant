from sqlmodel import SQLModel, Field
from datetime import datetime

class Order(SQLModel, table=True):
    __tablename__ = "orders"

    order_id: int | None = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="clients.client_id")
    waiter_id: int = Field(foreign_key="employees.employee_id")
    table_id: int | None = Field(default=None, foreign_key="restaurant_tables.table_id")
    total_amount: int
    status_id: int = Field(foreign_key="statuses_orders.status_id")
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: datetime | None = None
