import logging
from sqlmodel import SQLModel, Session
from app.database.database import engine
# Import all models so they are registered in SQLModel.metadata.
from app.models.clients_model import Client
from app.models.dishes_categories_model import Category
from app.models.dishes_ingredients_model import DishIngredient
from app.models.dishes_model import Dish
from app.models.employees_model import Employee
from app.models.inrgedients_model import Ingredient
from app.models.menus_dishes_model import MenuDish
from app.models.menus_model import Menu
from app.models.orders_items_model import OrderItem
from app.models.orders_model import Order
from app.models.positions_model import Position
from app.models.restaurant_tables_model import RestaurantTable
from app.models.roles_model import Role
from app.models.statuses_orders_model import StatusOrder
from app.models.statuses_tables_model import StatusTable
from app.models.users_model import User
from app.models.users_roles_model import UserRole
from app.models.waiters_tables_model import WaiterTable
from app.database.seed import seed_database

logger=logging.getLogger(__name__)
def initialize_database():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        seed_database(session)
    logger.info("Таблицы БД созданы/проверены")
