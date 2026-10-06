from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database.database import get_db

from app.models.dish import Dish
from app.schemas.dish import *
from app.models.dish_category import Category
from app.schemas.dish_category import *


router = APIRouter(
    prefix="/dishes_categories",
    tags=["Dishes Categories"]
)


@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """Выводит список всех категорий блюд"""
    return db.exec(select(Category)).all()


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    """Выводит категорию блюд по его идентификатору"""
    category = db.get(Category, category_id)

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return category


@router.get("/category/{category_id}/dishes", response_model=list[DishResponse])
def get_category_dishes_all(category_id: int, db: Session = Depends(get_db)):
    """Выводит все блюда выбранной категории"""
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    dishes = db.exec(
        select(Dish).where(Dish.category_dishes_id == category_id)
    ).all()

    return dishes


@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Создает новую категорию"""
    new_category = Category(
        name=category.name,
        description=category.description
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, category_data: CategoryUpdate, db: Session = Depends(get_db)):
    """Частично изменяет категорию"""
    category = db.get(Category, category_id)

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    if category_data.name is not None:
        category.name = category_data.name

    if category_data.description is not None:
        category.description = category_data.description

    db.commit()
    db.refresh(category)

    return category


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Удаляет категорию"""
    category = db.get(Category, category_id)

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    db.delete(category)
    db.commit()

    return {"message": "Category deleted successfully"}