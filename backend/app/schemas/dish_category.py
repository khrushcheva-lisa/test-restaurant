from sqlmodel import SQLModel
from typing import Optional

class CategoryResponse(SQLModel):
    category_dishes_id : int
    name : str
    description : str

    class Config:
        from_attributes = True

class CategoryCreate(SQLModel):
    name: str
    description: str

class CategoryUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None