from sqlmodel import SQLModel, Field

class StatusOrder(SQLModel, table=True):
    __tablename__ = "statuses_orders"

    status_order_id: int | None = Field(default=None, primary_key=True)
    name: str
