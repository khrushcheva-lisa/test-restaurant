from sqlmodel import Session, select
from app.models.users_model import User
from app.models.users_roles_model import UserRole
from app.models.roles_model import Role
from app.models.employees_model import Employee
from app.core.security import hash_password
from app.controllers.exceptions import NotFoundError, ConflictError
from app.controllers.utils import rollback_and_raise

class UserController:
    @staticmethod
    def get_all(session: Session):
        try: 
            return session.exec(select(User)).all()
        except Exception as exc: 
            rollback_and_raise(session, exc, "получение пользователей")
    @staticmethod
    def get_by_id(user_id: int, session: Session):
        try:
            user=session.get(User,user_id)
            if user is None: 
                raise NotFoundError("Пользователь с указанным ID не найден")
            return user
        except NotFoundError: 
            raise
        except Exception as exc: 
            rollback_and_raise(session, exc, "получение пользователя")
    @staticmethod
    def create(data, session: Session):
        try:
            if session.exec(select(User).where(User.login == data.login)).first(): 
                raise ConflictError("Пользователь с таким логином уже существует")
            if data.employee_id and session.get(Employee,data.employee_id) is None: 
                raise NotFoundError("Сотрудник с указанным ID не найден")
            role=session.get(Role,data.role_id)
            if role is None: 
                raise NotFoundError("Роль с указанным ID не найдена")
            user=User(login=data.login,password_hash=hash_password(data.password),employee_id=data.employee_id)
            session.add(user)
            session.flush()
            session.add(UserRole(user_id=user.user_id,role_id=role.role_id))
            session.commit()
            session.refresh(user)
            return user
        except (NotFoundError,ConflictError): 
            session.rollback()
            raise
        except Exception as exc: 
            rollback_and_raise(session,exc,"создание пользователя")
    @staticmethod
    def update(user_id: int, data, session: Session):
        try:
            user=session.get(User,user_id)
            if user is None: 
                raise NotFoundError("Пользователь с указанным ID не найден")
            values=data.model_dump(exclude_unset=True)
            if values.get("login") and session.exec(select(User).where(User.login==values["login"],User.user_id!=user_id)).first(): 
                raise ConflictError("Пользователь с таким логином уже существует")
            if "password" in values and values["password"]: 
                user.password_hash=hash_password(values.pop("password"))
            else: 
                values.pop("password",None)
            for key,value in values.items(): 
                setattr(user,key,value)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        except (NotFoundError,ConflictError): 
            session.rollback()
            raise
        except Exception as exc: 
            rollback_and_raise(session,exc,"изменение пользователя")
    @staticmethod
    def delete(user_id: int, session: Session):
        try:
            user=session.get(User,user_id)
            if user is None: 
                raise NotFoundError("Пользователь с указанным ID не найден")
            session.exec(select(UserRole).where(UserRole.user_id==user_id)).all()
            for link in session.exec(select(UserRole).where(UserRole.user_id==user_id)).all(): 
                session.delete(link)
            session.delete(user)
            session.commit()
        except NotFoundError: 
            raise
        except Exception as exc: 
            rollback_and_raise(session,exc,"удаление пользователя")
