from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.database.database import get_db
from app.core.validation import PositiveID
from app.api.errors import controller_http_error
from app.api.auth_router import manager_or_admin
from app.schemas.roles_schema import RoleCreate, RoleUpdate, RoleResponse
from app.controllers.roles_controller import RoleController

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/", response_model=list[RoleResponse])
def get_roles(db: Session = Depends(get_db)):
    try: return RoleController.get_all(db)
    except Exception as exc: raise controller_http_error(exc)


@router.get("/{role_id}", response_model=RoleResponse)
def get_role_by_id(role_id: PositiveID, db: Session = Depends(get_db)):
    try: return RoleController.get_by_id(role_id, db)
    except Exception as exc: raise controller_http_error(exc)

@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(data: RoleCreate, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    try: return RoleController.create(data, db)
    except Exception as exc: raise controller_http_error(exc)

@router.patch("/{role_id}", response_model=RoleResponse)
def update_role(role_id: PositiveID, data: RoleUpdate, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    try: return RoleController.update(role_id, data, db)
    except Exception as exc: raise controller_http_error(exc)

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: PositiveID, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    try: RoleController.delete(role_id, db); return None
    except Exception as exc: raise controller_http_error(exc)
