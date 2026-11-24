from datetime import date
from pydantic import BaseModel, ConfigDict, Field

class MenuCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=2, max_length=1000)
    valid_from: date
    valid_to: date
    is_active: bool = True

class MenuUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, min_length=2, max_length=1000)
    valid_from: date | None = None
    valid_to: date | None = None
    is_active: bool | None = None

class MenuResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    menu_id: int
    name: str
    description: str
    valid_from: date
    valid_to: date
    is_active: bool
    created_at: date
