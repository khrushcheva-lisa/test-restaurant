from fastapi import APIRouter,Depends,status
from sqlmodel import Session
from app.database.database import get_db
from app.schemas.dishes_ingredients_schema import DishIngredientCreate,DishIngredientUpdate,DishIngredientResponse
from app.api.auth_router import manager_or_admin
from app.core.validation import PositiveID
from app.controllers.dishes_ingredients_controller import DishIngredientController
from app.api.errors import controller_http_error

router=APIRouter(prefix="/dishes_ingredients",tags=["Dishes Ingredients"])
@router.get("/",response_model=list[DishIngredientResponse])
def get_dishes_ingredients(db:Session=Depends(get_db)):
    try:return DishIngredientController.get_all(db)
    except Exception as exc:raise controller_http_error(exc)
@router.get("/{dish_ingredient_id}",response_model=DishIngredientResponse)
def get_dish_ingredient_by_id(dish_ingredient_id:PositiveID,db:Session=Depends(get_db)):
    try:return DishIngredientController.get_by_id(dish_ingredient_id,db)
    except Exception as exc:raise controller_http_error(exc)
@router.post("/",response_model=DishIngredientResponse,status_code=status.HTTP_201_CREATED)
def create_dish_ingredient(data:DishIngredientCreate,db:Session=Depends(get_db),_=Depends(manager_or_admin)):
    try:return DishIngredientController.create(data,db)
    except Exception as exc:raise controller_http_error(exc)
@router.patch("/{dish_ingredient_id}",response_model=DishIngredientResponse)
def update_dish_ingredient(dish_ingredient_id:PositiveID,data:DishIngredientUpdate,db:Session=Depends(get_db),_=Depends(manager_or_admin)):
    try:return DishIngredientController.update(dish_ingredient_id,data,db)
    except Exception as exc:raise controller_http_error(exc)
@router.delete("/{dish_ingredient_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_dish_ingredient(dish_ingredient_id:PositiveID,db:Session=Depends(get_db),_=Depends(manager_or_admin)):
    try:DishIngredientController.delete(dish_ingredient_id,db);return None
    except Exception as exc:raise controller_http_error(exc)
