from sqlmodel import Session, select
from app.models.waiters_tables_model import WaiterTable
from app.models.employees_model import Employee
from app.controllers.crud_utils import get_all, get_one, create_one, update_one, delete_one
from app.controllers.exceptions import NotFoundError
from app.controllers.utils import rollback_and_raise

class WaiterTableController:
    @staticmethod
    def get_all(session: Session): 
        return get_all(session, WaiterTable, "получение назначений официантов")
    @staticmethod
    def get_by_id(assignment_id: int, session: Session): 
        return get_one(session, WaiterTable, assignment_id, "получение назначения", "Назначение")
    @staticmethod
    def create(data, session: Session): 
        return create_one(session, WaiterTable, data, "назначение официанта на стол")
    @staticmethod
    def update(assignment_id: int, data, session: Session): 
        return update_one(session, WaiterTable, assignment_id, data, "изменение назначения", "Назначение")
    @staticmethod
    def delete(assignment_id: int, session: Session): 
        return delete_one(session, WaiterTable, assignment_id, "удаление назначения", "Назначение")
    @staticmethod
    def get_waiter_tables(waiter_id: int, session: Session):
        try:
            if session.get(Employee, waiter_id) is None: 
                raise NotFoundError("Официант с указанным ID не найден")
            return session.exec(select(WaiterTable).where(WaiterTable.waiter_id == waiter_id, WaiterTable.unassigned_at.is_(None))).all()
        except NotFoundError: 
            raise
        except Exception as exc: 
            rollback_and_raise(session, exc, "получение столов официанта")
