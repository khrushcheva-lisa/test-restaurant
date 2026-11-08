from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.core.validation import DateTimeValidation

class OrderResponse(DateTimeValidation):
    model_config = ConfigDict(from_attributes=True)
    order_id: int
    client_id: int
    waiter_id: int
    total_amount: int
    status_id: int
    created_at: datetime
    completed_at: datetime | None = None


class OrderCreate(DateTimeValidation):

    model_config = ConfigDict(from_attributes=True)
    client_id: int = Field(gt=0, description="ID клиента", examples=[1, 2, 3])
    waiter_id: int = Field(gt=0, description="ID официанта", examples=[1, 2, 3])
    total_amount: int = Field(gt=0, description="Общая сумма заказа", examples=[1000, 2000, 3000])
    status_id: int = Field(gt=0, description="ID статуса", examples=[1, 2, 3])
    created_at: datetime = Field(default_factory=datetime.now, description="Время создания заказа")


class OrderUpdate(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    client_id: int | None = Field(default=None, gt=0, description="ID клиента", examples=[1, 2, 3])
    waiter_id: int | None = Field(default=None, gt=0, description="ID официанта", examples=[1, 2, 3])
    total_amount: int | None = Field(default=None, gt=0, description="Общая сумма заказа", examples=[1000, 2000, 3000])
    status_id: int | None = Field(default=None, gt=0, description="ID статуса", examples=[1, 2, 3])
    completed_at: datetime | None = Field(default=None, description="Время завершения заказа", examples=["2023-01-01T12:00:00"])

