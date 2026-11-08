from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from app.database.database import get_db
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
from app.models.employee import Employee
from app.core.security import hash_password
from app.core.security import (
    create_access_token, create_refresh_token, decode_token, verify_password,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class UserCreate(BaseModel):
    login: str = Field(min_length=3, max_length=50, pattern=r"^[A-Za-z0-9_.-]+$")
    password: str = Field(min_length=8, max_length=128)
    employee_id: int | None = Field(default=None, gt=0)
    role_id: int = Field(gt=0)


class UserRead(BaseModel):
    user_id: int
    login: str
    employee_id: int | None
    is_active: bool


@router.post("/login", response_model=TokenResponse, summary="Вход и получение пары JWT")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.login == form.username)).first()
    if user is None or not user.is_active or not verify_password(form.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenResponse(
        access_token=create_access_token(user.user_id),
        refresh_token=create_refresh_token(user.user_id),
    )


@router.post("/refresh", response_model=TokenResponse, summary="Обновить пару токенов")
def refresh_tokens(data: RefreshRequest, db: Session = Depends(get_db)):
    payload = decode_token(data.refresh_token, expected_type="refresh")
    if payload is None:
        raise HTTPException(status_code=401, detail="Недействительный или просроченный refresh-токен")
    user = db.get(User, int(payload["sub"]))
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="Пользователь не найден или заблокирован")
    return TokenResponse(
        access_token=create_access_token(user.user_id),
        refresh_token=create_refresh_token(user.user_id),
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    payload = decode_token(token, expected_type="access")
    if payload is None:
        raise HTTPException(status_code=401, detail="Недействительный или просроченный токен", headers={"WWW-Authenticate": "Bearer"})
    user = db.get(User, int(payload["sub"]))
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="Пользователь не найден или заблокирован", headers={"WWW-Authenticate": "Bearer"})
    return user



@router.get("/me", response_model=UserRead, summary="Текущий пользователь")
def get_me(user: User = Depends(get_current_user)):
    return user


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED, summary="Создать пользователя (только admin)")
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_user),
):
    if not get_user_roles(_admin, db).intersection({"admin", "администратор"}):
        raise HTTPException(status_code=403, detail="Создавать пользователей может только администратор")
    if db.exec(select(User).where(User.login == data.login)).first() is not None:
        raise HTTPException(status_code=409, detail="Такой логин уже существует")
    if data.employee_id is not None and db.get(Employee, data.employee_id) is None:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    role = db.get(Role, data.role_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    user = User(login=data.login, password_hash=hash_password(data.password), employee_id=data.employee_id)
    try:
        db.add(user)
        db.flush()
        db.add(UserRole(user_id=user.user_id, role_id=role.role_id))
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        raise

def get_user_roles(user: User, db: Session) -> set[str]:
    names = db.exec(
        select(Role.name)
        .join(UserRole, UserRole.role_id == Role.role_id)
        .where(UserRole.user_id == user.user_id)
    ).all()
    return {name.strip().lower() for name in names}


def require_roles(*allowed_roles: str):
    """Фабрика зависимости: проверяет, что у пользователя есть одна из ролей."""
    allowed = {role.strip().lower() for role in allowed_roles}

    def role_checker(
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:
        user_roles = get_user_roles(user, db)
        if not user_roles.intersection(allowed):
            raise HTTPException(status_code=403, detail="Недостаточно прав для выполнения операции")
        return user

    return role_checker


# Названия должны совпадать со значениями в таблице roles.name.
manager_or_admin = require_roles("manager", "admin", "менеджер", "администратор")
waiter_or_manager = require_roles("waiter", "manager", "admin", "официант", "менеджер", "администратор")
admin_only = require_roles("admin", "администратор")
