from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.database.database import get_db
from app.core.validation import PositiveID
from app.api.errors import controller_http_error
from app.api.auth_router import manager_or_admin
from app.schemas.menus_schema import MenuCreate, MenuUpdate, MenuResponse
from app.controllers.menus_controller import MenuController

router = APIRouter(prefix="/menu", tags=["Menu"])

@router.get("/", response_model=list[MenuResponse])
def get_menus(db: Session = Depends(get_db)):
    try: return MenuController.get_all(db)
    except Exception as exc: raise controller_http_error(exc)

@router.get("/active", response_model=list[MenuResponse])
def get_active_menu(db: Session = Depends(get_db)):
    try: return MenuController.get_active(db)
    except Exception as exc: raise controller_http_error(exc)

@router.get("/{menu_id}/dishes")
def get_menu_dishes(menu_id: PositiveID, db: Session = Depends(get_db)):
    try: return MenuController.get_dishes(menu_id, db)
    except Exception as exc: raise controller_http_error(exc)

@router.get("/{menu_id}", response_model=MenuResponse)
def get_menu_by_id(menu_id: PositiveID, db: Session = Depends(get_db)):
    try: return MenuController.get_by_id(menu_id, db)
    except Exception as exc: raise controller_http_error(exc)

@router.post("/", response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
def create_menu(data: MenuCreate, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    try: return MenuController.create(data, db)
    except Exception as exc: raise controller_http_error(exc)

@router.patch("/{menu_id}", response_model=MenuResponse)
def update_menu(menu_id: PositiveID, data: MenuUpdate, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    try: return MenuController.update(menu_id, data, db)
    except Exception as exc: raise controller_http_error(exc)

@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu(menu_id: PositiveID, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    try: MenuController.delete(menu_id, db); return None
    except Exception as exc: raise controller_http_error(exc)
