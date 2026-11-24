from sqlmodel import SQLModel, Field
from datetime import datetime

class WaiterTable(SQLModel, table=True):
    __tablename__ = "waiter_tables"

    waiter_table_id: int | None = Field(default=None, primary_key=True)
    waiter_id: int = Field(foreign_key="employees.employee_id")
    table_id: int = Field(foreign_key="restaurant_tables.table_id")
    assigned_at: datetime = Field(default_factory=datetime.now)
    unassigned_at: datetime | None = None
