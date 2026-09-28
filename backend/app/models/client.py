from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base

class Client(Base):
    __tablename__ = "clients"

    client_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    patronymic = Column(String)
    email = Column(String)
    phone = Column(String)
    created_at = Column(DateTime, default=func.now())