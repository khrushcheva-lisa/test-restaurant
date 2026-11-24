from sqlmodel import Session, select
from app.models.restaurant_tables_model import RestaurantTable
from app.models.statuses_tables_model import StatusTable
from app.controllers.crud_utils import get_all, get_one, create_one, update_one, delete_one
from app.controllers.utils import rollback_and_raise

class TableController:
    @staticmethod
    def get_all(session: Session): return get_all(session, RestaurantTable, "получение столов")
    @staticmethod
    def get_by_id(table_id: int, session: Session): return get_one(session, RestaurantTable, table_id, "получение стола", "Стол")
    @staticmethod
    def get_free(session: Session):
        try:
            free_status = session.exec(select(StatusTable).where(StatusTable.name.in_(["Свободен", "Свободный", "free"]))).first()
            if free_status is None: return []
            return session.exec(select(RestaurantTable).where(RestaurantTable.status_id == free_status.status_id)).all()
        except Exception as exc: rollback_and_raise(session, exc, "получение свободных столов")
    @staticmethod
    def create(data, session: Session): return create_one(session, RestaurantTable, data, "создание стола")
    @staticmethod
    def update(table_id: int, data, session: Session): return update_one(session, RestaurantTable, table_id, data, "изменение стола", "Стол")
    @staticmethod
    def delete(table_id: int, session: Session): return delete_one(session, RestaurantTable, table_id, "удаление стола", "Стол")
