from sqlmodel import Session, create_engine
from app.core.config import DATABASE_URL
import logging
from sqlmodel import SQLModel, Session
from app.database.seed import seed_database

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)


def get_db():
    """Создаёт отдельную сессию БД на время одного запроса."""
    with Session(engine) as session:
        yield session

logger=logging.getLogger(__name__)
def initialize_database():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        seed_database(session)
    logger.info("Таблицы БД созданы/проверены")
