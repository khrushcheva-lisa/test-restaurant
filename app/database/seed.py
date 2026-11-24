import logging
import random
from datetime import date, datetime, timedelta, timezone
from faker import Faker
from sqlmodel import Session, select
from app.models.positions_model import Position
from app.models.roles_model import Role
from app.models.statuses_orders_model import StatusOrder
from app.models.statuses_tables_model import StatusTable
from app.models.employees_model import Employee
from app.models.clients_model import Client
from app.models.users_model import User
from app.models.users_roles_model import UserRole
from app.models.restaurant_tables_model import RestaurantTable
from app.models.dishes_categories_model import Category
from app.models.dishes_model import Dish
from app.models.inrgedients_model import Ingredient
from app.models.dishes_ingredients_model import DishIngredient
from app.models.menus_model import Menu
from app.models.menus_dishes_model import MenuDish
from app.models.orders_model import Order
from app.models.orders_items_model import OrderItem
from app.models.waiters_tables_model import WaiterTable
from app.core.security import hash_password
from app.database.bootstrap_admin import ensure_admin

logger=logging.getLogger(__name__)
fake=Faker("ru_RU")
Faker.seed(2026)
random.seed(2026)

def seed_database(session: Session):
    """Заполняет только пустые таблицы. Повторный запуск не дублирует данные."""
    try:
        for name in ["Официант", "Менеджер", "Повар", "Администратор"]:
            if session.exec(select(Position).where(Position.name == name)).first() is None:
                session.add(Position(name=name))
        session.flush()
        position_by_name={p.name:p for p in session.exec(select(Position)).all()}

        required_roles=[("admin","Полный доступ к системе"),("manager","Управление рестораном"),("waiter","Работа с заказами и столами")]
        for name, description in required_roles:
            if session.exec(select(Role).where(Role.name == name)).first() is None:
                session.add(Role(name=name,description=description))
        session.flush()
        role_by_name={r.name:r for r in session.exec(select(Role)).all()}

        for name in ["Новый", "В работе", "Завершён", "Отменён"]:
            if session.exec(select(StatusOrder).where(StatusOrder.name == name)).first() is None:
                session.add(StatusOrder(name=name))
        for name in ["Свободен", "Занят", "Зарезервирован"]:
            if session.exec(select(StatusTable).where(StatusTable.name == name)).first() is None:
                session.add(StatusTable(name=name))
        session.flush()

        employees=session.exec(select(Employee)).all()
        if not employees:
            pos_waiter=position_by_name["Официант"].position_id
            pos_manager=position_by_name["Менеджер"].position_id
            pos_cook=position_by_name["Повар"].position_id
            employees=[]
            for i in range(15):
                employees.append(Employee(first_name=fake.first_name(),last_name=fake.last_name(),patronymic=fake.middle_name(),phone=fake.unique.phone_number()[:20],email=fake.unique.email(),position_id=pos_waiter,birth_date=fake.date_of_birth(minimum_age=19,maximum_age=55),hire_date=fake.date_between(start_date="-5y",end_date="today")))
            for pos_id in [pos_manager,pos_cook]:
                employees.append(Employee(first_name=fake.first_name(),last_name=fake.last_name(),patronymic=fake.middle_name(),phone=fake.unique.phone_number()[:20],email=fake.unique.email(),position_id=pos_id,birth_date=fake.date_of_birth(minimum_age=23,maximum_age=60),hire_date=fake.date_between(start_date="-5y",end_date="today")))
            session.add_all(employees); session.flush()

        role_waiter=role_by_name["waiter"]; role_manager=role_by_name["manager"]
        for employee in session.exec(select(Employee)).all():
            if session.exec(select(User).where(User.employee_id==employee.employee_id)).first(): continue
            pos=session.get(Position,employee.position_id)
            if not pos or pos.name not in {"Официант", "Менеджер"}: continue
            login=f"employee{employee.employee_id}"
            user=User(employee_id=employee.employee_id,login=login,password_hash=hash_password("Restaurant123!"),is_active=True)
            session.add(user); session.flush()
            chosen=role_manager if pos and pos.name=="Менеджер" else role_waiter
            session.add(UserRole(user_id=user.user_id,role_id=chosen.role_id))
        # Проверяем и создаём начального администратора из .env
        ensure_admin(session)

        if not session.exec(select(Client)).first():
            clients=[Client(first_name=fake.first_name(),last_name=fake.last_name(),patronymic=fake.middle_name(),phone=f"+7{fake.unique.random_number(digits=10,fix_len=True)}",email=fake.unique.email(),created_at=fake.date_between(start_date="-2y",end_date="today")) for _ in range(25)]
            session.add_all(clients); session.flush()
        if not session.exec(select(RestaurantTable)).first():
            free=session.exec(select(StatusTable).where(StatusTable.name=="Свободен")).first()
            session.add_all([RestaurantTable(seats_count=random.choice([2,2,4,4,6,8]),status_id=free.status_id) for _ in range(15)]); session.flush()
        if not session.exec(select(Category)).first():
            session.add_all([Category(name=n,description=d) for n,d in [("Салаты","Холодные блюда из овощей и других ингредиентов"),("Супы","Первые блюда"),("Горячее","Основные горячие блюда"),("Десерты","Сладкие блюда"),("Напитки","Холодные и горячие напитки")]]); session.flush()
        if not session.exec(select(Ingredient)).first():
            names=["Картофель","Морковь","Лук","Курица","Говядина","Помидор","Огурец","Сыр","Сливки","Мука","Яйцо","Рис","Макароны","Сахар","Яблоко","Салат","Зелень","Масло","Рыба","Лимон"]
            session.add_all([Ingredient(name=n) for n in names]); session.flush()
        if not session.exec(select(Dish)).first():
            cats=session.exec(select(Category)).all()
            dish_names=[("Цезарь с курицей",0,520,280),("Овощной салат",0,350,220),("Борщ",1,450,300),("Куриный суп",1,380,250),("Стейк",2,850,450),("Паста с сыром",2,560,320),("Чизкейк",3,390,180),("Яблочный пирог",3,320,160),("Морс",4,180,250),("Лимонад",4,210,300)]
            dishes=[Dish(category_dishes_id=cats[idx].category_dishes_id,name=name,description=f"Вкусное блюдо ресторана «{name}»",price=price,weight_grams=weight,is_active=True) for name,idx,price,weight in dish_names]
            session.add_all(dishes); session.flush()
        if not session.exec(select(DishIngredient)).first():
            ingredients=session.exec(select(Ingredient)).all(); dishes=session.exec(select(Dish)).all()
            session.add_all([DishIngredient(dish_id=d.dish_id,ingredient_id=ingredients[i%len(ingredients)].ingredient_id,quantity=random.choice([30,50,100,150])) for i,d in enumerate(dishes)])
        if not session.exec(select(Menu)).first():
            menu=Menu(name="Основное меню",description="Основное меню ресторана",valid_from=date.today()-timedelta(days=30),valid_to=date.today()+timedelta(days=365),is_active=True,created_at=date.today())
            session.add(menu); session.flush()
            session.add_all([MenuDish(menu_id=menu.menu_id,dish_id=d.dish_id) for d in session.exec(select(Dish)).all()])
        session.flush()
        if not session.exec(select(WaiterTable)).first():
            waiters=session.exec(select(Employee).join(Position).where(Position.name=="Официант")).all()
            tables=session.exec(select(RestaurantTable)).all()
            for table,waiter in zip(tables,waiters): session.add(WaiterTable(waiter_id=waiter.employee_id,table_id=table.table_id,assigned_at=datetime.now(timezone.utc)))
        session.flush()
        if not session.exec(select(Order)).first():
            clients=session.exec(select(Client)).all(); waiters=session.exec(select(Employee).join(Position).where(Position.name=="Официант")).all()
            status=session.exec(select(StatusOrder).where(StatusOrder.name=="Завершён")).first()
            dishes=session.exec(select(Dish)).all()
            for i in range(20):
                dish=random.choice(dishes); quantity=random.randint(1,3)
                order=Order(client_id=random.choice(clients).client_id,waiter_id=random.choice(waiters).employee_id,total_amount=dish.price*quantity,status_id=status.status_id,table_id=random.choice(session.exec(select(RestaurantTable)).all()).table_id,created_at=datetime.now()-timedelta(days=random.randint(0,30)))
                session.add(order); session.flush()
                session.add(OrderItem(order_id=order.order_id,dish_id=dish.dish_id,quantity=quantity,price=dish.price))
        session.commit()
        logger.info("Проверка и заполнение тестовых данных завершены")
    except Exception:
        session.rollback()
        logger.exception("Ошибка заполнения БД тестовыми данными")
        raise
