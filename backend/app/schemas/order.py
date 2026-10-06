from sqlmodel import SQLModel
from datetime import datetime
#from typing import Optional

class OrderResponse(SQLModel):
    order_id : int
    client_id : int
    waiter_id : int
    total_amount : int
    status_id : int
    created_at : datetime
    completed_at : datetime | None = None

    class Config:
        from_attributes = True