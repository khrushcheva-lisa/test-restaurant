from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from app.database.database import get_db
from app.models.dish import Dish
from app.schemas.dish import DishCreate, DishUpdate, DishResponse
from app.api.auth import manager_or_admin
from app.core.validation import PositiveID

router = APIRouter(prefix="/dishes", tags=["Dishes"])

@router.get("/", response_model=list[DishResponse])
def get_dishes(db: Session = Depends(get_db)):
    return db.exec(select(Dish)).all()

@router.get("/category/{category_id}", response_model=list[DishResponse])
def get_dishes_by_category(category_id: PositiveID, db: Session = Depends(get_db)):
    return db.exec(select(Dish).where(Dish.category_dishes_id == category_id)).all()

@router.get("/{dish_id}", response_model=DishResponse)
def get_dish_by_id(dish_id: PositiveID, db: Session = Depends(get_db)):
    dish = db.get(Dish, dish_id)
    if dish is None:
        raise HTTPException(status_code=404, detail="Dish not found")
    return dish

@router.post("/", response_model=DishResponse, status_code=status.HTTP_201_CREATED)
def create_dish(data: DishCreate, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    dish = Dish(**data.model_dump())
    try:
        db.add(dish)
        db.commit()
        db.refresh(dish)
        return dish
    except Exception:
        db.rollback()
        raise

@router.patch("/{dish_id}", response_model=DishResponse)
def update_dish(dish_id: PositiveID, data: DishUpdate, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    dish = db.get(Dish, dish_id)
    if dish is None:
        raise HTTPException(status_code=404, detail="Dish not found")
    for field, value in data.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(dish, field, value)
    try:
        db.add(dish)
        db.commit()
        db.refresh(dish)
        return dish
    except Exception:
        db.rollback()
        raise

@router.delete("/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dish(dish_id: PositiveID, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    dish = db.get(Dish, dish_id)
    if dish is None:
        raise HTTPException(status_code=404, detail="Dish not found")
    try:
        db.delete(dish)
        db.commit()
    except Exception:
        db.rollback()
        raise
