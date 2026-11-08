from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from app.database.database import get_db
from app.models.dish import Dish
from app.models.dish_category import Category
from app.schemas.dish import DishResponse
from app.schemas.dish_category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.api.auth import manager_or_admin
from app.core.validation import PositiveID

router = APIRouter(prefix="/dishes_categories", tags=["Dishes Categories"])

@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.exec(select(Category)).all()

@router.get("/category/{category_id}/dishes", response_model=list[DishResponse])
def get_category_dishes_all(category_id: PositiveID, db: Session = Depends(get_db)):
    if db.get(Category, category_id) is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db.exec(select(Dish).where(Dish.category_dishes_id == category_id)).all()

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category_by_id(category_id: PositiveID, db: Session = Depends(get_db)):
    category = db.get(Category, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(data: CategoryCreate, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    category = Category(**data.model_dump())
    try:
        db.add(category); db.commit(); db.refresh(category)
        return category
    except Exception:
        db.rollback(); raise

@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: PositiveID, data: CategoryUpdate, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    category = db.get(Category, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    for field, value in data.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(category, field, value)
    try:
        db.add(category); db.commit(); db.refresh(category)
        return category
    except Exception:
        db.rollback(); raise

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: PositiveID, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    category = db.get(Category, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    try:
        db.delete(category); db.commit()
    except Exception:
        db.rollback(); raise
