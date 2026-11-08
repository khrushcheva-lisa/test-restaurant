from sqlmodel import SQLModel, Field

class RestaurantTable(SQLModel, table=True):
    __tablename__ = "restaurant_tables"

    table_id: int | None = Field(default=None, primary_key=True)
    seats_count: int
    status_id: int | None = Field(default=None, foreign_key="table_statuses.status_id")