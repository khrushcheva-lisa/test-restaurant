from sqlalchemy import Column, Integer, String, Boolean, Text
from app.database import Base


class Dish(Base):
    __tablename__ = "dishes"

    dish_id = Column(Integer, primary_key=True)
    category_dishes_id = Column(Integer)   
    name = Column(String)
    description = Column(Text)
    price = Column(Integer)
    weight_grams = Column(Integer)
    is_active = Column(Boolean, default=True)