import logging
from sqlmodel import Session, select
from app.models.users_model import User
from app.models.roles_model import Role
from app.models.users_roles_model import UserRole
from app.models.employees_model import Employee
from app.core.security import hash_password, create_access_token, create_refresh_token, decode_token, verify_password
from app.controllers.exceptions import NotFoundError, ConflictError, UnauthorizedError, ForbiddenError
from app.controllers.utils import rollback_and_raise
from app.schemas.auth_schema import TokenResponse, UserCreate

logger=logging.getLogger(__name__)



class AuthController:
    @staticmethod
    def login(username: str,password: str,session: Session):
        try:
            user=session.exec(select(User).where(User.login==username)).first()
            if user is None or not user.is_active or not verify_password(password,user.password_hash):
                raise UnauthorizedError("Неверный логин или пароль")
            return TokenResponse(access_token=create_access_token(user.user_id),refresh_token=create_refresh_token(user.user_id))
        except UnauthorizedError: raise
        except Exception as exc: rollback_and_raise(session,exc,"вход пользователя")

    @staticmethod
    def refresh_tokens(refresh_token: str,session: Session):
        try:
            payload=decode_token(refresh_token,expected_type="refresh")
            if payload is None: raise UnauthorizedError("Недействительный или просроченный refresh-токен")
            try: user_id=int(payload["sub"])
            except (ValueError,TypeError,KeyError): raise UnauthorizedError("Некорректный refresh-токен")
            user=session.get(User,user_id)
            if user is None or not user.is_active: raise UnauthorizedError("Пользователь не найден или заблокирован")
            return TokenResponse(access_token=create_access_token(user.user_id),refresh_token=create_refresh_token(user.user_id))
        except UnauthorizedError: raise
        except Exception as exc: rollback_and_raise(session,exc,"обновление токенов")

    @staticmethod
    def get_current_user(token: str,session: Session):
        try:
            payload=decode_token(token,expected_type="access")
            if payload is None: raise UnauthorizedError("Недействительный или просроченный токен")
            try: user_id=int(payload["sub"])
            except (ValueError,TypeError,KeyError): raise UnauthorizedError("Некорректный токен")
            user=session.get(User,user_id)
            if user is None or not user.is_active: raise UnauthorizedError("Пользователь не найден или заблокирован")
            return user
        except UnauthorizedError: raise
        except Exception as exc: rollback_and_raise(session,exc,"проверка токена")

    @staticmethod
    def get_user_roles(user: User,session: Session) -> set[str]:
        try:
            names=session.exec(select(Role.name).join(UserRole,UserRole.role_id==Role.role_id).where(UserRole.user_id==user.user_id)).all()
            return {name.strip().lower() for name in names}
        except Exception as exc: rollback_and_raise(session,exc,"получение ролей пользователя")

    @staticmethod
    def create_user(data: UserCreate,session: Session):
        try:
            if session.exec(select(User).where(User.login==data.login)).first() is not None:
                raise ConflictError("Пользователь с таким логином уже существует")
            if data.employee_id is not None and session.get(Employee,data.employee_id) is None:
                raise NotFoundError("Сотрудник с указанным ID не найден")
            role=session.get(Role,data.role_id)
            if role is None: raise NotFoundError("Роль с указанным ID не найдена")
            user=User(login=data.login,password_hash=hash_password(data.password),employee_id=data.employee_id)
            session.add(user);session.flush();session.add(UserRole(user_id=user.user_id,role_id=role.role_id));session.commit();session.refresh(user)
            return user
        except (ConflictError,NotFoundError):
            session.rollback();raise
        except Exception as exc: rollback_and_raise(session,exc,"создание пользователя")
