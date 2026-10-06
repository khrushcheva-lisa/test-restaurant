from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database.database import get_db

from app.models.dish import Dish
from app.schemas.dish import *


router = APIRouter(
    prefix="/dishes",
    tags=["Dishes"]
)


@router.get("/", response_model=list[DishResponse])
def get_dishes(db: Session = Depends(get_db)):
    """Выводит список всех блюд"""
    return db.exec(select(Dish)).all()


@router.get("/{dish_id}", response_model=DishResponse)
def get_dish_by_id(dish_id: int, db: Session = Depends(get_db)):
    """Выводит блюдо по его идентификатору"""
    dish = db.get(Dish, dish_id)

    if not dish:
        raise HTTPException(
            status_code=404,
            detail="Dish not found"
        )

    return dish


@router.get("/category/{category_id}", response_model=list[DishResponse])
def get_dishes_by_category(category_id: int, db: Session = Depends(get_db)):
    """Выводит все блюда определённой категории"""
    dishes = db.exec(
        select(Dish).where(Dish.category_dishes_id == category_id)
    ).all()

    return dishes


@router.post("/", response_model=DishResponse)
def create_dish(dish: DishCreate, db: Session = Depends(get_db)):
    """Создает новое блюдо"""
    new_dish = Dish(
        category_dishes_id=dish.category_dishes_id,
        name=dish.name,
        description=dish.description,
        price=dish.price,
        weight_grams=dish.weight_grams,
        is_active=dish.is_active
    )

    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)

    return new_dish


@router.patch("/{dish_id}", response_model=DishResponse)
def update_dish(dish_id: int, dish_data: DishUpdate, db: Session = Depends(get_db)):
    """Частично изменяет блюдо"""
    dish = db.get(Dish, dish_id)

    if not dish:
        raise HTTPException(
            status_code=404,
            detail="Dish not found"
        )

    if dish_data.category_dishes_id is not None:
        dish.category_dishes_id = dish_data.category_dishes_id

    if dish_data.name is not None:
        dish.name = dish_data.name

    if dish_data.description is not None:
        dish.description = dish_data.description

    if dish_data.price is not None:
        dish.price = dish_data.price

    if dish_data.weight_grams is not None:
        dish.weight_grams = dish_data.weight_grams

    if dish_data.is_active is not None:
        dish.is_active = dish_data.is_active

    db.commit()
    db.refresh(dish)

    return dish


@router.delete("/{dish_id}")
def delete_dish(dish_id: int, db: Session = Depends(get_db)):
    """Удаляет блюдо"""
    dish = db.get(Dish, dish_id)

    if not dish:
        raise HTTPException(
            status_code=404,
            detail="Dish not found"
        )

    db.delete(dish)
    db.commit()

    return {"message": "Dish deleted successfully"}