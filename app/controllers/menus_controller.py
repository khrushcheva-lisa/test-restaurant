from datetime import date
from sqlmodel import Session, select
from app.models.menus_model import Menu
from app.models.menus_dishes_model import MenuDish
from app.models.dishes_model import Dish
from app.controllers.crud_utils import get_all, get_one, create_one, update_one, delete_one
from app.controllers.exceptions import NotFoundError, ConflictError
from app.controllers.utils import rollback_and_raise

class MenuController:
    @staticmethod
    def get_all(session: Session): return get_all(session, Menu, "получение меню")
    @staticmethod
    def get_by_id(menu_id: int, session: Session): return get_one(session, Menu, menu_id, "получение меню", "Меню")
    @staticmethod
    def get_active(session: Session):
        try: return session.exec(select(Menu).where(Menu.is_active == True, Menu.valid_from <= date.today(), Menu.valid_to >= date.today())).all()
        except Exception as exc: rollback_and_raise(session, exc, "получение действующего меню")
    @staticmethod
    def create(data, session: Session):
        if data.valid_to < data.valid_from: raise ConflictError("Дата окончания меню не может быть раньше даты начала")
        return create_one(session, Menu, data, "создание меню")
    @staticmethod
    def update(menu_id: int, data, session: Session):
        if data.valid_from and data.valid_to and data.valid_to < data.valid_from: raise ConflictError("Дата окончания меню не может быть раньше даты начала")
        return update_one(session, Menu, menu_id, data, "изменение меню", "Меню")
    @staticmethod
    def delete(menu_id: int, session: Session): return delete_one(session, Menu, menu_id, "удаление меню", "Меню")
    @staticmethod
    def get_dishes(menu_id: int, session: Session):
        try:
            if session.get(Menu, menu_id) is None: raise NotFoundError("Меню с указанным ID не найдено")
            return session.exec(select(Dish).join(MenuDish, MenuDish.dish_id == Dish.dish_id).where(MenuDish.menu_id == menu_id)).all()
        except NotFoundError: raise
        except Exception as exc: rollback_and_raise(session, exc, "получение блюд меню")
