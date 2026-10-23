from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database.database import get_db

from app.models.inrgedient import Ingredient
from app.models.dish import Dish
from app.models.dish_ingredient import DishIngredient
from app.schemas.dish import DishResponse
from app.schemas.ingredient import *


router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients"]
)


@router.get("/", response_model=list[IngredientResponse])
def get_ingredients(db: Session = Depends(get_db)):
    """Выводит список всех ингредиентов"""
    return db.exec(select(Ingredient)).all()


@router.get("/{ingredient_id}", response_model=IngredientResponse)
def get_ingredient_by_id(ingredient_id: int, db: Session = Depends(get_db)):
    """Выводит ингредиент по его идентификатору"""
    ingredient = db.get(Ingredient, ingredient_id)

    if not ingredient:
        raise HTTPException(
            status_code=404,
            detail="Ingredient not found"
        )

    return ingredient


@router.get("/{ingredient_id}/dishes", response_model=list[DishResponse])
def get_dishes_by_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    """Выводит все блюда, содержащие определенный ингредиент"""
    ingredient = db.get(Ingredient, ingredient_id)

    if not ingredient:
        raise HTTPException(
            status_code=404,
            detail="Ingredient not found"
        )

    dishes = db.exec(
        select(Dish)
        .join(DishIngredient, Dish.dish_id == DishIngredient.dish_id)
        .where(DishIngredient.ingredient_id == ingredient_id)
    ).all()

    return dishes


@router.post("/", response_model=IngredientResponse)
def create_ingredient(ingredient: IngredientCreate, db: Session = Depends(get_db)):
    """Создает новый ингредиент"""
    new_ingredient = Ingredient(
        name=ingredient.name
    )

    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)

    return new_ingredient


@router.patch("/{ingredient_id}", response_model=IngredientResponse)
def update_ingredient(ingredient_id: int, ingredient_data: IngredientUpdate, db: Session = Depends(get_db)):
    """Частично изменяет ингредиент"""
    ingredient = db.get(Ingredient, ingredient_id)

    if not ingredient:
        raise HTTPException(
            status_code=404,
            detail="Ingredient not found"
        )

    if ingredient_data.name is not None:
        ingredient.name = ingredient_data.name

    db.commit()
    db.refresh(ingredient)

    return ingredient


@router.delete("/{ingredient_id}")
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    """Удаляет ингредиент"""
    ingredient = db.get(Ingredient, ingredient_id)

    if not ingredient:
        raise HTTPException(
            status_code=404,
            detail="Ingredient not found"
        )

    db.delete(ingredient)
    db.commit()

    return {"message": "Ingredient deleted successfully"}