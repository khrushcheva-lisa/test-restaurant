import logging
from sqlmodel import Session, select
from app.models.clients_model import Client
from app.models.orders_model import Order
from app.controllers.exceptions import NotFoundError
from app.controllers.utils import rollback_and_raise

logger = logging.getLogger(__name__)

class ClientController:
    @staticmethod
    def get_clients(session: Session):
        try: return session.exec(select(Client)).all()
        except Exception as exc: rollback_and_raise(session, exc, "получение списка клиентов")

    @staticmethod
    def get_client_by_id(client_id: int, session: Session):
        try:
            client=session.get(Client, client_id)
            if client is None: raise NotFoundError("Клиент с указанным ID не найден")
            return client
        except NotFoundError: raise
        except Exception as exc: rollback_and_raise(session, exc, "получение клиента")

    @staticmethod
    def get_client_orders(client_id: int, session: Session):
        try:
            if session.get(Client, client_id) is None: raise NotFoundError("Клиент с указанным ID не найден")
            return session.exec(select(Order).where(Order.client_id == client_id)).all()
        except NotFoundError: raise
        except Exception as exc: rollback_and_raise(session, exc, "получение заказов клиента")

    @staticmethod
    def create_client(data, session: Session):
        try:
            client=Client(**data.model_dump()); session.add(client); session.commit(); session.refresh(client); return client
        except Exception as exc: rollback_and_raise(session, exc, "создание клиента")

    @staticmethod
    def update_client(client_id: int, data, session: Session):
        try:
            client=session.get(Client, client_id)
            if client is None: raise NotFoundError("Клиент с указанным ID не найден")
            for field,value in data.model_dump(exclude_unset=True, exclude_none=True).items(): setattr(client,field,value)
            session.add(client); session.commit(); session.refresh(client); return client
        except NotFoundError: raise
        except Exception as exc: rollback_and_raise(session, exc, "изменение клиента")

    @staticmethod
    def delete_client(client_id: int, session: Session):
        try:
            client=session.get(Client, client_id)
            if client is None: raise NotFoundError("Клиент с указанным ID не найден")
            session.delete(client); session.commit()
        except NotFoundError: raise
        except Exception as exc: rollback_and_raise(session, exc, "удаление клиента")
