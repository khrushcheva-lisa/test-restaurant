from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session
from app.database.database import get_db
from app.models.users_model import User
from app.controllers.auth_controller import AuthController
from app.schemas.auth_schema import TokenResponse, RefreshRequest, UserCreate, UserRead
from app.api.errors import controller_http_error
from app.controllers.exceptions import ForbiddenError

router=APIRouter(prefix="/auth",tags=["Authentication"])
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/login",response_model=TokenResponse,summary="Вход и получение пары JWT")
def login(form:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    try:return AuthController.login(form.username,form.password,db)
    except Exception as exc:raise controller_http_error(exc)

@router.post("/refresh",response_model=TokenResponse,summary="Обновить пару токенов")
def refresh_tokens(data:RefreshRequest,db:Session=Depends(get_db)):
    try:return AuthController.refresh_tokens(data.refresh_token,db)
    except Exception as exc:raise controller_http_error(exc)

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db))->User:
    try:return AuthController.get_current_user(token,db)
    except Exception as exc:raise controller_http_error(exc)

@router.get("/me",response_model=UserRead,summary="Текущий пользователь")
def get_me(user:User=Depends(get_current_user)):
    return user

@router.post("/users",response_model=UserRead,status_code=status.HTTP_201_CREATED,summary="Создать пользователя (только admin)")
def create_user(data:UserCreate,db:Session=Depends(get_db),admin:User=Depends(get_current_user)):
    try:
        if not AuthController.get_user_roles(admin,db).intersection({"admin","администратор"}):
            raise ForbiddenError("Создавать пользователей может только администратор")
        return AuthController.create_user(data,db)
    except Exception as exc:raise controller_http_error(exc)

def require_roles(*allowed_roles:str):
    allowed={role.strip().lower() for role in allowed_roles}
    def role_checker(user:User=Depends(get_current_user),db:Session=Depends(get_db))->User:
        try:
            if not AuthController.get_user_roles(user,db).intersection(allowed):
                raise ForbiddenError("Недостаточно прав для выполнения операции")
            return user
        except Exception as exc:raise controller_http_error(exc)
    return role_checker

manager_or_admin=require_roles("manager","admin","менеджер","администратор")
waiter_or_manager=require_roles("waiter","manager","admin","официант","менеджер","администратор")
admin_only=require_roles("admin","администратор")
