from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.dish import Dish
from app.schemas.dish import DishResponse


router = APIRouter(
    prefix="/dishes",
    tags=["Dishes"]
)


@router.get("/", response_model=list[DishResponse])
def get_dishes(db: Session = Depends(get_db)):
    return db.query(Dish).all()