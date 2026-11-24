from sqlmodel import Session, select
from app.models.orders_model import Order
from app.models.clients_model import Client
from app.models.employees_model import Employee
from app.models.restaurant_tables_model import RestaurantTable
from app.models.waiters_tables_model import WaiterTable
from app.controllers.crud_utils import get_all, get_one, create_one, update_one, delete_one
from app.controllers.exceptions import NotFoundError
from app.controllers.utils import rollback_and_raise

class OrderController:
    @staticmethod
    def get_all(session: Session): return get_all(session, Order, "получение заказов")
    @staticmethod
    def get_by_id(order_id: int, session: Session): return get_one(session, Order, order_id, "получение заказа", "Заказ")
    @staticmethod
    def create(data, session: Session): return create_one(session, Order, data, "создание заказа")
    @staticmethod
    def update(order_id: int, data, session: Session): return update_one(session, Order, order_id, data, "изменение заказа", "Заказ")
    @staticmethod
    def delete(order_id: int, session: Session): return delete_one(session, Order, order_id, "отмена заказа", "Заказ")
    @staticmethod
    def by_client(client_id: int, session: Session):
        try:
            if session.get(Client, client_id) is None: raise NotFoundError("Клиент с указанным ID не найден")
            return session.exec(select(Order).where(Order.client_id == client_id)).all()
        except NotFoundError: raise
        except Exception as exc: rollback_and_raise(session, exc, "получение заказов клиента")
    @staticmethod
    def by_waiter(waiter_id: int, session: Session):
        try:
            if session.get(Employee, waiter_id) is None: raise NotFoundError("Сотрудник с указанным ID не найден")
            return session.exec(select(Order).where(Order.waiter_id == waiter_id)).all()
        except NotFoundError: raise
        except Exception as exc: rollback_and_raise(session, exc, "получение заказов официанта")
    @staticmethod
    def by_table(table_id: int, session: Session):
        try:
            if session.get(RestaurantTable, table_id) is None: raise NotFoundError("Стол с указанным ID не найден")
            return session.exec(select(Order).where(Order.table_id == table_id)).all()
        except NotFoundError: raise
        except Exception as exc: rollback_and_raise(session, exc, "получение заказов стола")
