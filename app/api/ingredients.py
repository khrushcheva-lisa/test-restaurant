from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from app.database.database import get_db
from app.models.inrgedient import Ingredient
from app.models.dish import Dish
from app.models.dish_ingredient import DishIngredient
from app.schemas.dish import DishResponse
from app.schemas.ingredient import IngredientCreate, IngredientUpdate, IngredientResponse
from app.api.auth import manager_or_admin
from app.core.validation import PositiveID

router = APIRouter(prefix="/ingredients", tags=["Ingredients"])

@router.get("/", response_model=list[IngredientResponse])
def get_ingredients(db: Session = Depends(get_db)):
    return db.exec(select(Ingredient)).all()

@router.get("/{ingredient_id}/dishes", response_model=list[DishResponse])
def get_dishes_by_ingredient(ingredient_id: PositiveID, db: Session = Depends(get_db)):
    if db.get(Ingredient, ingredient_id) is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return db.exec(select(Dish).join(DishIngredient, Dish.dish_id == DishIngredient.dish_id).where(DishIngredient.ingredient_id == ingredient_id)).all()

@router.get("/{ingredient_id}", response_model=IngredientResponse)
def get_ingredient_by_id(ingredient_id: PositiveID, db: Session = Depends(get_db)):
    ingredient = db.get(Ingredient, ingredient_id)
    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient

@router.post("/", response_model=IngredientResponse, status_code=status.HTTP_201_CREATED)
def create_ingredient(data: IngredientCreate, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    ingredient = Ingredient(**data.model_dump())
    try:
        db.add(ingredient); db.commit(); db.refresh(ingredient)
        return ingredient
    except Exception:
        db.rollback(); raise

@router.patch("/{ingredient_id}", response_model=IngredientResponse)
def update_ingredient(ingredient_id: PositiveID, data: IngredientUpdate, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    ingredient = db.get(Ingredient, ingredient_id)
    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    for field, value in data.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(ingredient, field, value)
    try:
        db.add(ingredient); db.commit(); db.refresh(ingredient)
        return ingredient
    except Exception:
        db.rollback(); raise

@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(ingredient_id: PositiveID, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    ingredient = db.get(Ingredient, ingredient_id)
    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    try:
        db.delete(ingredient); db.commit()
    except Exception:
        db.rollback(); raise
