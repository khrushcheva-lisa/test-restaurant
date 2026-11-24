from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.database.database import get_db
from app.core.validation import PositiveID
from app.api.errors import controller_http_error
from app.api.auth_router import manager_or_admin
from app.schemas.waiter_tables_schema import WaiterTableCreate, WaiterTableUpdate, WaiterTableResponse
from app.controllers.waiter_tables_controller import WaiterTableController

router = APIRouter(prefix="/waiter-tables", tags=["Waiter Tables"])

@router.get("/", response_model=list[WaiterTableResponse])
def get_waiter_tables(db: Session = Depends(get_db)):
    try: return WaiterTableController.get_all(db)
    except Exception as exc: raise controller_http_error(exc)

@router.get("/{assignment_id}", response_model=WaiterTableResponse)
def get_waiter_table_by_id(assignment_id: PositiveID, db: Session = Depends(get_db)):
    try: return WaiterTableController.get_by_id(assignment_id, db)
    except Exception as exc: raise controller_http_error(exc)

@router.post("/", response_model=WaiterTableResponse, status_code=status.HTTP_201_CREATED)
def create_waiter_table(data: WaiterTableCreate, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    try: return WaiterTableController.create(data, db)
    except Exception as exc: raise controller_http_error(exc)

@router.patch("/{assignment_id}", response_model=WaiterTableResponse)
def update_waiter_table(assignment_id: PositiveID, data: WaiterTableUpdate, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    try: return WaiterTableController.update(assignment_id, data, db)
    except Exception as exc: raise controller_http_error(exc)

@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_waiter_table(assignment_id: PositiveID, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    try: WaiterTableController.delete(assignment_id, db); return None
    except Exception as exc: raise controller_http_error(exc)
