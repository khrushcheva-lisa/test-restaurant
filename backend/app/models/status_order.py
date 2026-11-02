from sqlmodel import SQLModel, Field

class StatusOrder(SQLModel, table=True):
    __tablename__ = "table_statuses"

    status_id: int | None = Field(default=None, primary_key=True)
    name: str