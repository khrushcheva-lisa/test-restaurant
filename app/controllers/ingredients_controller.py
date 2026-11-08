from sqlmodel import Session, select
from app.models.inrgedients_model import Ingredient
from app.models.dishes_model import Dish
from app.models.dishes_ingredients_model import DishIngredient
from app.controllers.exceptions import NotFoundError
from app.controllers.utils import rollback_and_raise

class IngredientController:
    @staticmethod
    def get_ingredients(session: Session):
        try: return session.exec(select(Ingredient)).all()
        except Exception as exc: rollback_and_raise(session,exc,"получение ингредиентов")
    @staticmethod
    def get_ingredient_by_id(ingredient_id: int, session: Session):
        try:
            item=session.get(Ingredient,ingredient_id)
            if item is None: raise NotFoundError("Ингредиент с указанным ID не найден")
            return item
        except NotFoundError: raise
        except Exception as exc: rollback_and_raise(session,exc,"получение ингредиента")
    @staticmethod
    def get_dishes_by_ingredient(ingredient_id: int, session: Session):
        try:
            if session.get(Ingredient,ingredient_id) is None: raise NotFoundError("Ингредиент с указанным ID не найден")
            return session.exec(select(Dish).join(DishIngredient,Dish.dish_id==DishIngredient.dish_id).where(DishIngredient.ingredient_id==ingredient_id)).all()
        except NotFoundError: raise
        except Exception as exc: rollback_and_raise(session,exc,"получение блюд по ингредиенту")
    @staticmethod
    def create_ingredient(data, session: Session):
        try:
            item=Ingredient(**data.model_dump()); session.add(item); session.commit(); session.refresh(item); return item
        except Exception as exc: rollback_and_raise(session,exc,"создание ингредиента")
    @staticmethod
    def update_ingredient(ingredient_id: int, data, session: Session):
        try:
            item=session.get(Ingredient,ingredient_id)
            if item is None: raise NotFoundError("Ингредиент с указанным ID не найден")
            for field,value in data.model_dump(exclude_unset=True,exclude_none=True).items(): setattr(item,field,value)
            session.add(item); session.commit(); session.refresh(item); return item
        except NotFoundError: raise
        except Exception as exc: rollback_and_raise(session,exc,"изменение ингредиента")
    @staticmethod
    def delete_ingredient(ingredient_id: int, session: Session):
        try:
            item=session.get(Ingredient,ingredient_id)
            if item is None: raise NotFoundError("Ингредиент с указанным ID не найден")
            session.delete(item); session.commit()
        except NotFoundError: raise
        except Exception as exc: rollback_and_raise(session,exc,"удаление ингредиента")
