class ControllerError(Exception):
    """Базовая ошибка бизнес-логики."""

class NotFoundError(ControllerError):
    """Запрашиваемая запись не найдена."""

class ConflictError(ControllerError):
    """Конфликт или нарушение целостности данных."""

class DatabaseUnavailableError(ControllerError):
    """База данных временно недоступна."""

class DatabaseOperationError(ControllerError):
    """Ошибка выполнения операции с базой данных."""

class UnauthorizedError(ControllerError):
    """Ошибка аутентификации."""

class ForbiddenError(ControllerError):
    """Недостаточно прав."""
