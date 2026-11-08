from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.database.database import get_db
from app.schemas.clients_schema import ClientCreate, ClientUpdate, ClientResponse
from app.schemas.orders_schema import OrderResponse
from app.api.auth_router import get_current_user, waiter_or_manager, manager_or_admin
from app.core.validation import PositiveID
from app.controllers.clients_controller import ClientController
from app.api.errors import controller_http_error

router=APIRouter(prefix="/clients",tags=["Clients"])

@router.get("/",response_model=list[ClientResponse])
def get_clients(db:Session=Depends(get_db),_=Depends(get_current_user)):
    try: return ClientController.get_clients(db)
    except Exception as exc: raise controller_http_error(exc)

@router.get("/{client_id}/orders",response_model=list[OrderResponse])
def get_client_all_orders(client_id:PositiveID,db:Session=Depends(get_db),_=Depends(get_current_user)):
    try: return ClientController.get_client_orders(client_id,db)
    except Exception as exc: raise controller_http_error(exc)

@router.get("/{client_id}",response_model=ClientResponse)
def get_client_by_id(client_id:PositiveID,db:Session=Depends(get_db),_=Depends(get_current_user)):
    try: return ClientController.get_client_by_id(client_id,db)
    except Exception as exc: raise controller_http_error(exc)

@router.post("/",response_model=ClientResponse,status_code=status.HTTP_201_CREATED)
def create_client(data:ClientCreate,db:Session=Depends(get_db),_=Depends(waiter_or_manager)):
    try: return ClientController.create_client(data,db)
    except Exception as exc: raise controller_http_error(exc)

@router.patch("/{client_id}",response_model=ClientResponse)
def update_client(client_id:PositiveID,data:ClientUpdate,db:Session=Depends(get_db),_=Depends(manager_or_admin)):
    try: return ClientController.update_client(client_id,data,db)
    except Exception as exc: raise controller_http_error(exc)

@router.delete("/{client_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id:PositiveID,db:Session=Depends(get_db),_=Depends(manager_or_admin)):
    try: ClientController.delete_client(client_id,db); return None
    except Exception as exc: raise controller_http_error(exc)
