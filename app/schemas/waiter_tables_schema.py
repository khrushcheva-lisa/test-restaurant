from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class WaiterTableCreate(BaseModel):
    waiter_id: int = Field(gt=0)
    table_id: int = Field(gt=0)
    assigned_at: datetime | None = None

class WaiterTableUpdate(BaseModel):
    waiter_id: int | None = Field(default=None, gt=0)
    table_id: int | None = Field(default=None, gt=0)
    unassigned_at: datetime | None = None

class WaiterTableResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    waiter_table_id: int
    waiter_id: int
    table_id: int
    assigned_at: datetime
    unassigned_at: datetime | None
