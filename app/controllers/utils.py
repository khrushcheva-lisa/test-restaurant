import logging
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from app.controllers.exceptions import ConflictError, DatabaseOperationError, DatabaseUnavailableError

logger = logging.getLogger(__name__)

def rollback_and_raise(session, exc: Exception, operation: str):
    session.rollback()
    if isinstance(exc, IntegrityError):
        logger.warning("Нарушение целостности данных (%s): %s", operation, exc)
        raise ConflictError("Операция нарушает целостность данных: возможно, запись уже существует или на неё ссылаются другие записи") from exc
    if isinstance(exc, OperationalError):
        logger.exception("База данных недоступна (%s)", operation)
        raise DatabaseUnavailableError("База данных временно недоступна. Повторите запрос позже") from exc
    if isinstance(exc, SQLAlchemyError):
        logger.exception("Ошибка базы данных (%s)", operation)
        raise DatabaseOperationError("Не удалось выполнить операцию с базой данных") from exc
    logger.exception("Неожиданная ошибка контроллера (%s)", operation)
    raise
