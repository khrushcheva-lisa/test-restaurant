from pydantic import BaseModel, ConfigDict, Field

class OrderItemCreate(BaseModel):
    order_id: int = Field(gt=0)
    dish_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)

class OrderItemUpdate(BaseModel):
    order_id: int | None = Field(default=None, gt=0)
    dish_id: int | None = Field(default=None, gt=0)
    quantity: int | None = Field(default=None, gt=0)
    price: float | None = Field(default=None, gt=0)

class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    order_item_id: int
    order_id: int
    dish_id: int
    quantity: int
    price: float
