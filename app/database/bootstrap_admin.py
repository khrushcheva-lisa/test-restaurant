
import os
import logging
from datetime import date

from dotenv import load_dotenv
from sqlmodel import Session, select

from app.models.positions_model import Position
from app.models.employees_model import Employee
from app.models.users_model import User
from app.models.roles_model import Role
from app.models.users_roles_model import UserRole

from app.core.security import hash_password


logger = logging.getLogger(__name__)

load_dotenv()


def ensure_admin(session: Session):
    """Проверяет и при необходимости создаёт начального администратора."""

    # Получаем настройки из .env
    login = os.getenv("ADMIN_LOGIN")
    password = os.getenv("ADMIN_PASSWORD")

    first_name = os.getenv("ADMIN_FIRST_NAME")
    last_name = os.getenv("ADMIN_LAST_NAME")
    patronymic = os.getenv("ADMIN_PATRONYMIC") or None
    phone = os.getenv("ADMIN_PHONE")
    email = os.getenv("ADMIN_EMAIL")
    birth_date = os.getenv("ADMIN_BIRTH_DATE")
    hire_date = os.getenv("ADMIN_HIRE_DATE")

    required_values = {
        "ADMIN_LOGIN": login,
        "ADMIN_PASSWORD": password,
        "ADMIN_FIRST_NAME": first_name,
        "ADMIN_LAST_NAME": last_name,
        "ADMIN_PHONE": phone,
        "ADMIN_EMAIL": email,
        "ADMIN_BIRTH_DATE": birth_date,
        "ADMIN_HIRE_DATE": hire_date,
    }

    missing = [
        key for key, value in required_values.items()
        if not value or not value.strip()
    ]

    if missing:
        raise RuntimeError(
            "Не заполнены обязательные настройки администратора в .env: "
            + ", ".join(missing)
        )

    if len(password) < 8:
        raise RuntimeError(
            "Пароль начального администратора должен содержать минимум 8 символов"
        )

    admin_position = session.exec(
        select(Position).where(Position.name == "Администратор")
    ).first()

    if admin_position is None:
        raise RuntimeError(
            "В БД отсутствует должность «Администратор»"
        )

    admin_role = session.exec(
        select(Role).where(Role.name == "admin")
    ).first()

    if admin_role is None:
        raise RuntimeError(
            "В БД отсутствует роль admin"
        )

    employee = session.exec(
        select(Employee).where(Employee.email == email)
    ).first()

    if employee is None:
        employee = Employee(
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            phone=phone,
            email=email,
            position_id=admin_position.position_id,
            birth_date=date.fromisoformat(birth_date),
            hire_date=date.fromisoformat(hire_date),
        )

        session.add(employee)
        session.flush()

        logger.info(
            "Создан сотрудник начального администратора: ID %s",
            employee.employee_id
        )

    login_owner = session.exec(
        select(User).where(User.login == login)
    ).first()

    if (
        login_owner is not None
        and login_owner.employee_id != employee.employee_id
    ):
        raise RuntimeError(
            f"Логин '{login}' уже используется другим сотрудником "
            f"(Employee ID: {login_owner.employee_id})."
        )

    users = session.exec(
        select(User).where(
            User.employee_id == employee.employee_id
        )
    ).all()

    if len(users) > 1:
        raise RuntimeError(
            f"У сотрудника ID {employee.employee_id} обнаружено "
            f"несколько учётных записей. Необходимо устранить дублирование."
        )

    user = users[0] if users else None

    if user is None:

        existing_login = session.exec(
            select(User).where(User.login == login)
        ).first()

        if existing_login is not None:
            raise RuntimeError(
                f"Логин '{login}' уже принадлежит другому пользователю. "
                "Укажите другой ADMIN_LOGIN в .env."
            )

        user = User(
            employee_id=employee.employee_id,
            login=login,
            password_hash=hash_password(password),
            is_active=True,
        )

        session.add(user)
        session.flush()

        logger.info(
            "Создан пользователь начального администратора: ID %s",
            user.user_id
        )

    else:
        if user.login != login:
            logger.warning(
                "Логин пользователя ID %s отличается: "
                "в БД = '%s', в .env = '%s'. "
                "Существующий логин сохранён.",
                user.user_id,
                user.login,
                login
            )

        if not user.is_active:
            raise RuntimeError(
                f"Учётная запись администратора ID {user.user_id} "
                "неактивна. Автоматическая активация запрещена."
            )

    user_admin_role = session.exec(
        select(UserRole).where(
            UserRole.user_id == user.user_id,
            UserRole.role_id == admin_role.role_id
        )
    ).first()

    if user_admin_role is None:
        session.add(
            UserRole(
                user_id=user.user_id,
                role_id=admin_role.role_id
            )
        )

        logger.info(
            "Пользователю ID %s назначена роль admin",
            user.user_id
        )

    session.flush()

    logger.info(
        "Проверка начального администратора завершена. User ID: %s",
        user.user_id
    )
