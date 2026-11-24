from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database.database import get_db
from app.core.validation import PositiveID
from app.api.errors import controller_http_error
from app.schemas.waiter_tables_schema import WaiterTableResponse
from app.controllers.waiter_tables_controller import WaiterTableController

router=APIRouter(prefix="/waiters",tags=["Waiters"])
@router.get("/{waiter_id}/tables",response_model=list[WaiterTableResponse])
def get_waiter_tables(waiter_id:PositiveID,db:Session=Depends(get_db)):
    try:return WaiterTableController.get_waiter_tables(waiter_id,db)
    except Exception as exc:raise controller_http_error(exc)
