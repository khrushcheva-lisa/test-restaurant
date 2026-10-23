from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database.database import get_db

from app.models.dish_ingredient import DishIngredient
from app.schemas.dish_ingredient import *



router = APIRouter(
    prefix="/dishes_ingredients",
    tags=["Dishes Ingredients"]
)


@router.get("/", response_model=list[DishIngredientResponse])
def get_dishes_ingredients(db: Session = Depends(get_db)):
    """Выводит список всех связей между блюдами и ингредиентами"""
    return db.exec(select(DishIngredient)).all()


@router.get("/{dish_ingredient_id}", response_model=DishIngredientResponse)
def get_dish_ingredient_by_id(dish_ingredient_id: int, db: Session = Depends(get_db)):
    """Выводит связь между блюдом и ингредиентом по его идентификатору"""
    dish_ingredient = db.get(DishIngredient, dish_ingredient_id)

    if not dish_ingredient:
        raise HTTPException(
            status_code=404,
            detail="Dish ingredient not found"
        )

    return dish_ingredient



@router.post("/", response_model=DishIngredientResponse)
def create_dish_ingredient(dish_ingredient: DishIngredientCreate, db: Session = Depends(get_db)):
    """Создает новую связь между блюдом и ингредиентом"""
    new_dish_ingredient = DishIngredient(
        ingredient_id=dish_ingredient.ingredient_id,
        dish_id=dish_ingredient.dish_id,
        quantity=dish_ingredient.quantity
    )

    db.add(new_dish_ingredient)
    db.commit()
    db.refresh(new_dish_ingredient)

    return new_dish_ingredient


@router.patch("/{dish_ingredient_id}", response_model=DishIngredientResponse)
def update_dish_ingredient(dish_ingredient_id: int, dish_ingredient_data: DishIngredientUpdate, db: Session = Depends(get_db)):
    """Частично изменяет связь между блюдом и ингредиентом"""
    dish_ingredient = db.get(DishIngredient, dish_ingredient_id)

    if not dish_ingredient:
        raise HTTPException(
            status_code=404,
            detail="Dish ingredient not found"
        )

    if dish_ingredient_data.quantity is not None:
        dish_ingredient.quantity = dish_ingredient_data.quantity

    db.commit()
    db.refresh(dish_ingredient)

    return dish_ingredient


@router.delete("/{dish_ingredient_id}")
def delete_dish_ingredient(dish_ingredient_id: int, db: Session = Depends(get_db)):
    """Удаляет связь между блюдом и ингредиентом"""
    dish_ingredient = db.get(DishIngredient, dish_ingredient_id)

    if not dish_ingredient:
        raise HTTPException(
            status_code=404,
            detail="Dish ingredient not found"
        )

    db.delete(dish_ingredient)
    db.commit()

    return {"message": "Dish ingredient deleted successfully"}