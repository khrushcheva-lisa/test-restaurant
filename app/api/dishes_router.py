from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.database.database import get_db
from app.schemas.dishes_schema import DishCreate,DishUpdate,DishResponse
from app.api.auth_router import manager_or_admin
from app.core.validation import PositiveID
from app.controllers.dishes_controller import DishController
from app.api.errors import controller_http_error

router=APIRouter(prefix="/dishes",tags=["Dishes"])
@router.get("/",response_model=list[DishResponse])
def get_dishes(db:Session=Depends(get_db)):
    try:return DishController.get_dishes(db)
    except Exception as exc:raise controller_http_error(exc)
@router.get("/category/{category_id}",response_model=list[DishResponse])
def get_dishes_by_category(category_id:PositiveID,db:Session=Depends(get_db)):
    try:return DishController.get_dishes_by_category(category_id,db)
    except Exception as exc:raise controller_http_error(exc)
@router.get("/{dish_id}",response_model=DishResponse)
def get_dish_by_id(dish_id:PositiveID,db:Session=Depends(get_db)):
    try:return DishController.get_dish_by_id(dish_id,db)
    except Exception as exc:raise controller_http_error(exc)
@router.post("/",response_model=DishResponse,status_code=status.HTTP_201_CREATED)
def create_dish(data:DishCreate,db:Session=Depends(get_db),_=Depends(manager_or_admin)):
    try:return DishController.create_dish(data,db)
    except Exception as exc:raise controller_http_error(exc)
@router.patch("/{dish_id}",response_model=DishResponse)
def update_dish(dish_id:PositiveID,data:DishUpdate,db:Session=Depends(get_db),_=Depends(manager_or_admin)):
    try:return DishController.update_dish(dish_id,data,db)
    except Exception as exc:raise controller_http_error(exc)
@router.delete("/{dish_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_dish(dish_id:PositiveID,db:Session=Depends(get_db),_=Depends(manager_or_admin)):
    try:DishController.delete_dish(dish_id,db);return None
    except Exception as exc:raise controller_http_error(exc)
