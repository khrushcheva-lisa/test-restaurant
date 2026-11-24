from sqlmodel import Session
from app.models.roles_model import Role
from app.controllers.crud_utils import get_all, get_one, create_one, update_one, delete_one

class RoleController:
    @staticmethod
    def get_all(session: Session): 
        return get_all(session, Role, "получение ролей")
    @staticmethod
    def get_by_id(role_id: int, session: Session): 
        return get_one(session, Role, role_id, "получение роли", "Роль")
    @staticmethod
    def create(data, session: Session): 
        return create_one(session, Role, data, "создание роли")
    @staticmethod
    def update(role_id: int, data, session: Session): 
        return update_one(session, Role, role_id, data, "изменение роли", "Роль")
    @staticmethod
    def delete(role_id: int, session: Session): 
        return delete_one(session, Role, role_id, "удаление роли", "Роль")
