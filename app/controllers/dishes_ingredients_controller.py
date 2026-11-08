from sqlmodel import Session, select
from app.models.dishes_ingredients_model import DishIngredient
from app.controllers.exceptions import NotFoundError
from app.controllers.utils import rollback_and_raise

class DishIngredientController:
    @staticmethod
    def get_all(session: Session):
        try: return session.exec(select(DishIngredient)).all()
        except Exception as exc: rollback_and_raise(session,exc,"получение составов блюд")
    @staticmethod
    def get_by_id(item_id: int, session: Session):
        try:
            item=session.exec(select(DishIngredient).where(DishIngredient.dish_ingredient_id==item_id)).first()
            if item is None: raise NotFoundError("Связь блюда с ингредиентом не найдена")
            return item
        except NotFoundError: raise
        except Exception as exc: rollback_and_raise(session,exc,"получение состава блюда")
    @staticmethod
    def create(data, session: Session):
        try:
            item=DishIngredient(**data.model_dump()); session.add(item); session.commit(); session.refresh(item); return item
        except Exception as exc: rollback_and_raise(session,exc,"добавление ингредиента в блюдо")
    @staticmethod
    def update(item_id: int, data, session: Session):
        try:
            item=session.exec(select(DishIngredient).where(DishIngredient.dish_ingredient_id==item_id)).first()
            if item is None: raise NotFoundError("Связь блюда с ингредиентом не найдена")
            for field,value in data.model_dump(exclude_unset=True,exclude_none=True).items(): setattr(item,field,value)
            session.add(item); session.commit(); session.refresh(item); return item
        except NotFoundError: raise
        except Exception as exc: rollback_and_raise(session,exc,"изменение состава блюда")
    @staticmethod
    def delete(item_id: int, session: Session):
        try:
            item=session.exec(select(DishIngredient).where(DishIngredient.dish_ingredient_id==item_id)).first()
            if item is None: raise NotFoundError("Связь блюда с ингредиентом не найдена")
            session.delete(item); session.commit()
        except NotFoundError: raise
        except Exception as exc: rollback_and_raise(session,exc,"удаление ингредиента из блюда")
