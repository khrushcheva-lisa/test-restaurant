from sqlmodel import Session, select
from app.models.dishes_model import Dish
from app.models.dishes_categories_model import Category
from app.controllers.exceptions import NotFoundError
from app.controllers.utils import rollback_and_raise

class CategoryController:
    @staticmethod
    def get_categories(session: Session):
        try: return session.exec(select(Category)).all()
        except Exception as exc: rollback_and_raise(session,exc,"получение категорий")
    @staticmethod
    def get_category_by_id(category_id: int, session: Session):
        try:
            item=session.get(Category,category_id)
            if item is None: raise NotFoundError("Категория с указанным ID не найдена")
            return item
        except NotFoundError: raise
        except Exception as exc: rollback_and_raise(session,exc,"получение категории")
    @staticmethod
    def get_category_dishes(category_id: int, session: Session):
        try:
            if session.get(Category,category_id) is None: raise NotFoundError("Категория с указанным ID не найдена")
            return session.exec(select(Dish).where(Dish.category_dishes_id==category_id)).all()
        except NotFoundError: raise
        except Exception as exc: rollback_and_raise(session,exc,"получение блюд категории")
    @staticmethod
    def create_category(data, session: Session):
        try:
            item=Category(**data.model_dump()); session.add(item); session.commit(); session.refresh(item); return item
        except Exception as exc: rollback_and_raise(session,exc,"создание категории")
    @staticmethod
    def update_category(category_id: int, data, session: Session):
        try:
            item=session.get(Category,category_id)
            if item is None: raise NotFoundError("Категория с указанным ID не найдена")
            for field,value in data.model_dump(exclude_unset=True,exclude_none=True).items(): setattr(item,field,value)
            session.add(item); session.commit(); session.refresh(item); return item
        except NotFoundError: raise
        except Exception as exc: rollback_and_raise(session,exc,"изменение категории")
    @staticmethod
    def delete_category(category_id: int, session: Session):
        try:
            item=session.get(Category,category_id)
            if item is None: raise NotFoundError("Категория с указанным ID не найдена")
            session.delete(item); session.commit()
        except NotFoundError: raise
        except Exception as exc: rollback_and_raise(session,exc,"удаление категории")
