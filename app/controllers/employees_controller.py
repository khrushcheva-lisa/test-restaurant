from sqlmodel import Session, select
from app.models.employees_model import Employee
from app.models.positions_model import Position
from app.controllers.crud_utils import get_all, get_one, create_one, update_one, delete_one
from app.controllers.exceptions import NotFoundError
from app.controllers.utils import rollback_and_raise

class EmployeeController:
    @staticmethod
    def get_all(session: Session): return get_all(session, Employee, "получение сотрудников")
    @staticmethod
    def get_by_id(employee_id: int, session: Session): return get_one(session, Employee, employee_id, "получение сотрудника", "Сотрудник")
    @staticmethod
    def get_by_position(position_name: str, session: Session):
        try: return session.exec(select(Employee).join(Position).where(Position.name == position_name)).all()
        except Exception as exc: rollback_and_raise(session, exc, "получение сотрудников по должности")
    @staticmethod
    def create(data, session: Session): return create_one(session, Employee, data, "создание сотрудника")
    @staticmethod
    def update(employee_id: int, data, session: Session): return update_one(session, Employee, employee_id, data, "изменение сотрудника", "Сотрудник")
    @staticmethod
    def delete(employee_id: int, session: Session): return delete_one(session, Employee, employee_id, "удаление сотрудника", "Сотрудник")
