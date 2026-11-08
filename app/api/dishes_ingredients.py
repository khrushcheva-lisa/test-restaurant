from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from app.database.database import get_db
from app.models.dish_ingredient import DishIngredient
from app.schemas.dish_ingredient import DishIngredientCreate, DishIngredientUpdate, DishIngredientResponse
from app.api.auth import manager_or_admin
from app.core.validation import PositiveID

router = APIRouter(prefix="/dishes_ingredients", tags=["Dishes Ingredients"])

@router.get("/", response_model=list[DishIngredientResponse])
def get_dishes_ingredients(db: Session = Depends(get_db)):
    return db.exec(select(DishIngredient)).all()

@router.get("/{dish_ingredient_id}", response_model=DishIngredientResponse)
def get_dish_ingredient_by_id(dish_ingredient_id: PositiveID, db: Session = Depends(get_db)):
    item = db.get(DishIngredient, dish_ingredient_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Dish ingredient not found")
    return item

@router.post("/", response_model=DishIngredientResponse, status_code=status.HTTP_201_CREATED)
def create_dish_ingredient(data: DishIngredientCreate, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    item = DishIngredient(**data.model_dump())
    try:
        db.add(item); db.commit(); db.refresh(item)
        return item
    except Exception:
        db.rollback(); raise

@router.patch("/{dish_ingredient_id}", response_model=DishIngredientResponse)
def update_dish_ingredient(dish_ingredient_id: PositiveID, data: DishIngredientUpdate, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    item = db.get(DishIngredient, dish_ingredient_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Dish ingredient not found")
    for field, value in data.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(item, field, value)
    try:
        db.add(item); db.commit(); db.refresh(item)
        return item
    except Exception:
        db.rollback(); raise

@router.delete("/{dish_ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dish_ingredient(dish_ingredient_id: PositiveID, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    item = db.get(DishIngredient, dish_ingredient_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Dish ingredient not found")
    try:
        db.delete(item); db.commit()
    except Exception:
        db.rollback(); raise
