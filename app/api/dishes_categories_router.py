from fastapi import APIRouter,Depends,status
from sqlmodel import Session
from app.database.database import get_db
from app.schemas.dishes_schema import DishResponse
from app.schemas.dishes_categories_schema import CategoryCreate,CategoryUpdate,CategoryResponse
from app.api.auth_router import manager_or_admin
from app.core.validation import PositiveID
from app.controllers.dishes_categories_controller import CategoryController
from app.api.errors import controller_http_error

router=APIRouter(prefix="/dishes_categories",tags=["Dishes Categories"])
@router.get("/",response_model=list[CategoryResponse])
def get_categories(db:Session=Depends(get_db)):
    try:return CategoryController.get_categories(db)
    except Exception as exc:raise controller_http_error(exc)
@router.get("/category/{category_id}/dishes",response_model=list[DishResponse])
def get_category_dishes_all(category_id:PositiveID,db:Session=Depends(get_db)):
    try:return CategoryController.get_category_dishes(category_id,db)
    except Exception as exc:raise controller_http_error(exc)
@router.get("/{category_id}",response_model=CategoryResponse)
def get_category_by_id(category_id:PositiveID,db:Session=Depends(get_db)):
    try:return CategoryController.get_category_by_id(category_id,db)
    except Exception as exc:raise controller_http_error(exc)
@router.post("/",response_model=CategoryResponse,status_code=status.HTTP_201_CREATED)
def create_category(data:CategoryCreate,db:Session=Depends(get_db),_=Depends(manager_or_admin)):
    try:return CategoryController.create_category(data,db)
    except Exception as exc:raise controller_http_error(exc)
@router.patch("/{category_id}",response_model=CategoryResponse)
def update_category(category_id:PositiveID,data:CategoryUpdate,db:Session=Depends(get_db),_=Depends(manager_or_admin)):
    try:return CategoryController.update_category(category_id,data,db)
    except Exception as exc:raise controller_http_error(exc)
@router.delete("/{category_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id:PositiveID,db:Session=Depends(get_db),_=Depends(manager_or_admin)):
    try:CategoryController.delete_category(category_id,db);return None
    except Exception as exc:raise controller_http_error(exc)
