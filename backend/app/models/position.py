from sqlmodel import SQLModel, Field

class Position(SQLModel, table=True):
    __tablename__ = "positions"

    position_id: int | None = Field(default=None, primary_key=True)
    name: str