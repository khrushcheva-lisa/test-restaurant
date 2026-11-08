from sqlmodel import SQLModel, Field
from datetime import datetime

class WaiterTable(SQLModel, table=True):
    __tablename__ = "waiter_tables"

    waiter_table_id: int | None = Field(default=None, primary_key=True)
    waiter_id: int | None = Field(default=None, foreign_key="users.user_id")
    table_id: int | None = Field(default=None, foreign_key="restaurant_tables.table_id")
    assigned_at: datetime = Field(default=datetime.now())
    unassigned_at: datetime | None = Field(default=None)