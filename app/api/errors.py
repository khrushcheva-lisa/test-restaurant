import logging
from fastapi import HTTPException, status
from app.controllers.exceptions import ConflictError, DatabaseOperationError, DatabaseUnavailableError, NotFoundError, UnauthorizedError, ForbiddenError

logger = logging.getLogger(__name__)

def controller_http_error(exc: Exception) -> HTTPException:
    if isinstance(exc, UnauthorizedError):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc), headers={"WWW-Authenticate": "Bearer"})
    if isinstance(exc, ForbiddenError):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))
    if isinstance(exc, NotFoundError):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    if isinstance(exc, ConflictError):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    if isinstance(exc, DatabaseUnavailableError):
        return HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc))
    if isinstance(exc, DatabaseOperationError):
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    logger.exception("Необработанная ошибка при выполнении API-запроса", exc_info=exc)
    return HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
