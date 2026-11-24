from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.database.database import get_db
from app.core.validation import PositiveID
from app.api.errors import controller_http_error
from app.api.auth_router import manager_or_admin, waiter_or_manager
from app.schemas.orders_schema import OrderCreate, OrderUpdate, OrderResponse
from app.controllers.orders_controller import OrderController
from app.controllers.order_items_controller import OrderItemController
from app.schemas.order_items_schema import OrderItemResponse

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    try: return OrderController.get_all(db)
    except Exception as exc: raise controller_http_error(exc)

@router.get("/client/{client_id}", response_model=list[OrderResponse])
def get_client_orders(client_id: PositiveID, db: Session = Depends(get_db)):
    try: return OrderController.by_client(client_id, db)
    except Exception as exc: raise controller_http_error(exc)

@router.get("/waiter/{waiter_id}", response_model=list[OrderResponse])
def get_waiter_orders(waiter_id: PositiveID, db: Session = Depends(get_db)):
    try: return OrderController.by_waiter(waiter_id, db)
    except Exception as exc: raise controller_http_error(exc)

@router.get("/table/{table_id}", response_model=list[OrderResponse])
def get_table_orders(table_id: PositiveID, db: Session = Depends(get_db)):
    try: return OrderController.by_table(table_id, db)
    except Exception as exc: raise controller_http_error(exc)

@router.get("/{order_id}", response_model=OrderResponse)
def get_order_by_id(order_id: PositiveID, db: Session = Depends(get_db)):
    try: return OrderController.get_by_id(order_id, db)
    except Exception as exc: raise controller_http_error(exc)

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(data: OrderCreate, db: Session = Depends(get_db), _=Depends(waiter_or_manager)):
    try: return OrderController.create(data, db)
    except Exception as exc: raise controller_http_error(exc)

@router.patch("/{order_id}", response_model=OrderResponse)
def update_order(order_id: PositiveID, data: OrderUpdate, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    try: return OrderController.update(order_id, data, db)
    except Exception as exc: raise controller_http_error(exc)

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: PositiveID, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    try: OrderController.delete(order_id, db); return None
    except Exception as exc: raise controller_http_error(exc)


@router.get("/{order_id}/dishes", response_model=list[OrderItemResponse])
def get_order_dishes(order_id: PositiveID, db: Session = Depends(get_db)):
    try: return OrderItemController.by_order(order_id, db)
    except Exception as exc: raise controller_http_error(exc)
