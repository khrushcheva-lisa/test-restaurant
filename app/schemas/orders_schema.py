from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    order_id: int
    client_id: int
    waiter_id: int
    table_id: int | None = None
    total_amount: int
    status_id: int
    created_at: datetime
    completed_at: datetime | None = None

class OrderCreate(BaseModel):
    client_id: int = Field(gt=0)
    waiter_id: int = Field(gt=0)
    table_id: int | None = Field(default=None, gt=0)
    total_amount: int = Field(gt=0)
    status_id: int = Field(gt=0)
    created_at: datetime | None = None
    completed_at: datetime | None = None

class OrderUpdate(BaseModel):
    client_id: int | None = Field(default=None, gt=0)
    waiter_id: int | None = Field(default=None, gt=0)
    table_id: int | None = Field(default=None, gt=0)
    total_amount: int | None = Field(default=None, gt=0)
    status_id: int | None = Field(default=None, gt=0)
    completed_at: datetime | None = None
