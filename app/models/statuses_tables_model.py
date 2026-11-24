from sqlmodel import SQLModel, Field

class StatusTable(SQLModel, table=True):
    __tablename__ = "statuses_tables"

    status_table_id: int | None = Field(default=None, primary_key=True)
    name: str
