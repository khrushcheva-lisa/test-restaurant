from sqlmodel import Session, select
from app.models.orders_items_model import OrderItem
from app.models.orders_model import Order
from app.controllers.crud_utils import get_all, get_one, create_one, update_one, delete_one
from app.controllers.exceptions import NotFoundError
from app.controllers.utils import rollback_and_raise

class OrderItemController:
    @staticmethod
    def get_all(session: Session): 
        return get_all(session, OrderItem, "получение блюд в заказах")
    @staticmethod
    def get_by_id(item_id: int, session: Session): return get_one(session, OrderItem, item_id, "получение позиции заказа", "Позиция заказа")
    @staticmethod
    def create(data, session: Session): 
        return create_one(session, OrderItem, data, "добавление блюда в заказ")
    @staticmethod
    def update(item_id: int, data, session: Session): return update_one(session, OrderItem, item_id, data, "изменение позиции заказа", "Позиция заказа")
    @staticmethod
    def delete(item_id: int, session: Session): 
        return delete_one(session, OrderItem, item_id, "удаление позиции заказа", "Позиция заказа")
    @staticmethod
    def by_order(order_id: int, session: Session):
        try:
            if session.get(Order, order_id) is None: 
                raise NotFoundError("Заказ с указанным ID не найден")
            return session.exec(select(OrderItem).where(OrderItem.order_id == order_id)).all()
        except NotFoundError: 
            raise
        except Exception as exc: 
            rollback_and_raise(session, exc, "получение блюд заказа")
