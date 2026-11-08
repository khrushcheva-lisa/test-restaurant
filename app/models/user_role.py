from sqlmodel import SQLModel, Field

class UserRole(SQLModel, table=True):
    __tablename__ = "users_roles"

    user_role_id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.user_id")
    role_id: int | None = Field(default=None, foreign_key="roles.role_id")