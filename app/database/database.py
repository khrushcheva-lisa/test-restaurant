from sqlmodel import Session, create_engine
from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)


def get_db():
    """Создаёт отдельную сессию БД на время одного запроса."""
    with Session(engine) as session:
        yield session
