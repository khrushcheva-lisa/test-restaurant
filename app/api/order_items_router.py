from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.database.database import get_db
from app.core.validation import PositiveID
from app.api.errors import controller_http_error
from app.api.auth_router import manager_or_admin, waiter_or_manager
from app.schemas.order_items_schema import OrderItemCreate, OrderItemUpdate, OrderItemResponse
from app.controllers.order_items_controller import OrderItemController

router=APIRouter(prefix="/order-items",tags=["Order Items"])
@router.get("/",response_model=list[OrderItemResponse])
def get_items(db:Session=Depends(get_db)):
    try:return OrderItemController.get_all(db)
    except Exception as exc:raise controller_http_error(exc)
@router.get("/{item_id}",response_model=OrderItemResponse)
def get_item(item_id:PositiveID,db:Session=Depends(get_db)):
    try:return OrderItemController.get_by_id(item_id,db)
    except Exception as exc:raise controller_http_error(exc)
@router.post("/",response_model=OrderItemResponse,status_code=status.HTTP_201_CREATED)
def create_item(data:OrderItemCreate,db:Session=Depends(get_db),_=Depends(waiter_or_manager)):
    try:return OrderItemController.create(data,db)
    except Exception as exc:raise controller_http_error(exc)
@router.patch("/{item_id}",response_model=OrderItemResponse)
def update_item(item_id:PositiveID,data:OrderItemUpdate,db:Session=Depends(get_db),_=Depends(manager_or_admin)):
    try:return OrderItemController.update(item_id,data,db)
    except Exception as exc:raise controller_http_error(exc)
@router.delete("/{item_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id:PositiveID,db:Session=Depends(get_db),_=Depends(manager_or_admin)):
    try:OrderItemController.delete(item_id,db);return None
    except Exception as exc:raise controller_http_error(exc)
