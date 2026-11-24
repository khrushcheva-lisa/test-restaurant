from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.database.database import get_db
from app.core.validation import PositiveID
from app.api.errors import controller_http_error
from app.api.auth_router import manager_or_admin
from app.schemas.tables_schema import TableCreate, TableUpdate, TableResponse
from app.controllers.tables_controller import TableController

router = APIRouter(prefix="/tables", tags=["Tables"])

@router.get("/", response_model=list[TableResponse])
def get_tables(db: Session = Depends(get_db)):
    try: return TableController.get_all(db)
    except Exception as exc: raise controller_http_error(exc)

@router.get("/free", response_model=list[TableResponse])
def get_free_tables(db: Session = Depends(get_db)):
    try: return TableController.get_free(db)
    except Exception as exc: raise controller_http_error(exc)

@router.get("/{table_id}", response_model=TableResponse)
def get_table_by_id(table_id: PositiveID, db: Session = Depends(get_db)):
    try: return TableController.get_by_id(table_id, db)
    except Exception as exc: raise controller_http_error(exc)

@router.post("/", response_model=TableResponse, status_code=status.HTTP_201_CREATED)
def create_table(data: TableCreate, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    try: return TableController.create(data, db)
    except Exception as exc: raise controller_http_error(exc)

@router.patch("/{table_id}", response_model=TableResponse)
def update_table(table_id: PositiveID, data: TableUpdate, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    try: return TableController.update(table_id, data, db)
    except Exception as exc: raise controller_http_error(exc)

@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_table(table_id: PositiveID, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    try: TableController.delete(table_id, db); return None
    except Exception as exc: raise controller_http_error(exc)
