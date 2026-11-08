from fastapi import APIRouter,Depends,status
from sqlmodel import Session
from app.database.database import get_db
from app.schemas.dishes_schema import DishResponse
from app.schemas.ingredients_schema import IngredientCreate,IngredientUpdate,IngredientResponse
from app.api.auth_router import manager_or_admin
from app.core.validation import PositiveID
from app.controllers.ingredients_controller import IngredientController
from app.api.errors import controller_http_error

router=APIRouter(prefix="/ingredients",tags=["Ingredients"])
@router.get("/",response_model=list[IngredientResponse])
def get_ingredients(db:Session=Depends(get_db)):
    try:return IngredientController.get_ingredients(db)
    except Exception as exc:raise controller_http_error(exc)
@router.get("/{ingredient_id}/dishes",response_model=list[DishResponse])
def get_dishes_by_ingredient(ingredient_id:PositiveID,db:Session=Depends(get_db)):
    try:return IngredientController.get_dishes_by_ingredient(ingredient_id,db)
    except Exception as exc:raise controller_http_error(exc)
@router.get("/{ingredient_id}",response_model=IngredientResponse)
def get_ingredient_by_id(ingredient_id:PositiveID,db:Session=Depends(get_db)):
    try:return IngredientController.get_ingredient_by_id(ingredient_id,db)
    except Exception as exc:raise controller_http_error(exc)
@router.post("/",response_model=IngredientResponse,status_code=status.HTTP_201_CREATED)
def create_ingredient(data:IngredientCreate,db:Session=Depends(get_db),_=Depends(manager_or_admin)):
    try:return IngredientController.create_ingredient(data,db)
    except Exception as exc:raise controller_http_error(exc)
@router.patch("/{ingredient_id}",response_model=IngredientResponse)
def update_ingredient(ingredient_id:PositiveID,data:IngredientUpdate,db:Session=Depends(get_db),_=Depends(manager_or_admin)):
    try:return IngredientController.update_ingredient(ingredient_id,data,db)
    except Exception as exc:raise controller_http_error(exc)
@router.delete("/{ingredient_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(ingredient_id:PositiveID,db:Session=Depends(get_db),_=Depends(manager_or_admin)):
    try:IngredientController.delete_ingredient(ingredient_id,db);return None
    except Exception as exc:raise controller_http_error(exc)
