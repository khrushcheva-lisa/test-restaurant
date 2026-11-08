import logging
from sqlmodel import Session, select
from app.models.dishes_model import Dish
from app.controllers.exceptions import NotFoundError
from app.controllers.utils import rollback_and_raise

logger=logging.getLogger(__name__)
class DishController:
    @staticmethod
    def get_dishes(session: Session):
        try: return session.exec(select(Dish)).all()
        except Exception as exc: rollback_and_raise(session,exc,"получение списка блюд")
    @staticmethod
    def get_dishes_by_category(category_id: int, session: Session):
        try: return session.exec(select(Dish).where(Dish.category_dishes_id==category_id)).all()
        except Exception as exc: rollback_and_raise(session,exc,"получение блюд категории")
    @staticmethod
    def get_dish_by_id(dish_id: int, session: Session):
        try:
            item=session.get(Dish,dish_id)
            if item is None: raise NotFoundError("Блюдо с указанным ID не найдено")
            return item
        except NotFoundError: raise
        except Exception as exc: rollback_and_raise(session,exc,"получение блюда")
    @staticmethod
    def create_dish(data, session: Session):
        try:
            item=Dish(**data.model_dump()); session.add(item); session.commit(); session.refresh(item); return item
        except Exception as exc: rollback_and_raise(session,exc,"создание блюда")
    @staticmethod
    def update_dish(dish_id: int, data, session: Session):
        try:
            item=session.get(Dish,dish_id)
            if item is None: raise NotFoundError("Блюдо с указанным ID не найдено")
            for field,value in data.model_dump(exclude_unset=True,exclude_none=True).items(): setattr(item,field,value)
            session.add(item); session.commit(); session.refresh(item); return item
        except NotFoundError: raise
        except Exception as exc: rollback_and_raise(session,exc,"изменение блюда")
    @staticmethod
    def delete_dish(dish_id: int, session: Session):
        try:
            item=session.get(Dish,dish_id)
            if item is None: raise NotFoundError("Блюдо с указанным ID не найдено")
            session.delete(item); session.commit()
        except NotFoundError: raise
        except Exception as exc: rollback_and_raise(session,exc,"удаление блюда")
