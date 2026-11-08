"""Одноразовое создание первого администратора: python -m scripts.create_admin"""

from getpass import getpass
from sqlmodel import Session, select

from app.database.database import engine
from app.models.user import User
from app.models.employee import Employee
from app.models.role import Role
from app.models.user_role import UserRole
from app.core.security import hash_password


def main():
    login = input("Логин администратора: ").strip()
    password = getpass("Пароль (минимум 8 символов): ")
    confirmation = getpass("Повторите пароль: ")

    if len(password) < 8 or password != confirmation:
        raise SystemExit("Пароли не совпадают или короче 8 символов")

    with Session(engine) as db:

        # Проверяем, существует ли пользователь
        if db.exec(select(User).where(User.login == login)).first():
            raise SystemExit("Пользователь с таким логином уже существует")

        # ПОЛУЧАЕМ ID СОТРУДНИКА
        employee_id = int(input("ID сотрудника для администратора: "))

        employee = db.get(Employee, employee_id)

        if employee is None:
            raise SystemExit("Сотрудник с таким ID не найден")

        # Ищем роль администратора
        role = db.exec(select(Role).where(Role.name == "admin")).first()

        if role is None:
            role = Role(
                name="admin",
                description="Полный доступ к системе"
            )
            db.add(role)
            db.flush()

        # СОЗДАЁМ ПОЛЬЗОВАТЕЛЯ С ПРИВЯЗКОЙ К СОТРУДНИКУ
        user = User(
            employee_id=employee.employee_id,
            login=login,
            password_hash=hash_password(password),
            is_active=True
        )

        try:
            db.add(user)
            db.flush()

            db.add(UserRole(
                user_id=user.user_id,
                role_id=role.role_id
            ))

            db.commit()

            print(f"Администратор '{login}' успешно создан. ID: {user.user_id}")

        except Exception:
            db.rollback()
            raise


if __name__ == "__main__":
    main()