from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.database.database import get_db
from app.core.validation import PositiveID
from app.api.auth_router import admin_only
from app.api.errors import controller_http_error
from app.schemas.users_schema import UserCreate, UserUpdate, UserResponse
from app.controllers.users_controller import UserController

router=APIRouter(prefix="/users",tags=["Users"])
@router.get("/{user_id}",response_model=UserResponse)
def get_user(user_id:PositiveID,db:Session=Depends(get_db),_=Depends(admin_only)):
    try:return UserController.get_by_id(user_id,db)
    except Exception as exc:raise controller_http_error(exc)
@router.patch("/{user_id}",response_model=UserResponse)
def update_user(user_id:PositiveID,data:UserUpdate,db:Session=Depends(get_db),_=Depends(admin_only)):
    try:return UserController.update(user_id,data,db)
    except Exception as exc:raise controller_http_error(exc)
@router.delete("/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id:PositiveID,db:Session=Depends(get_db),_=Depends(admin_only)):
    try:UserController.delete(user_id,db);return None
    except Exception as exc:raise controller_http_error(exc)
