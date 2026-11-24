from pydantic import BaseModel, ConfigDict, Field

class TableCreate(BaseModel):
    seats_count: int = Field(gt=0, le=30)
    status_id: int = Field(gt=0)

class TableUpdate(BaseModel):
    seats_count: int | None = Field(default=None, gt=0, le=30)
    status_id: int | None = Field(default=None, gt=0)

class TableResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    table_id: int
    seats_count: int
    status_id: int | None
