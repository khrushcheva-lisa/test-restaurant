from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from app.database.database import get_db
from app.models.client import Client
from app.models.order import Order
from app.schemas.client import ClientCreate, ClientUpdate, ClientResponse
from app.schemas.order import OrderResponse
from app.api.auth import get_current_user, waiter_or_manager, manager_or_admin
from app.core.validation import PositiveID

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("/", response_model=list[ClientResponse])
def get_clients(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.exec(select(Client)).all()

@router.get("/{client_id}/orders", response_model=list[OrderResponse])
def get_client_all_orders(client_id: PositiveID, db: Session = Depends(get_db), _=Depends(get_current_user)):
    if db.get(Client, client_id) is None:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return db.exec(select(Order).where(Order.client_id == client_id)).all()

@router.get("/{client_id}", response_model=ClientResponse)
def get_client_by_id(client_id: PositiveID, db: Session = Depends(get_db), _=Depends(get_current_user)):
    client = db.get(Client, client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return client

@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(data: ClientCreate, db: Session = Depends(get_db), _=Depends(waiter_or_manager)):
    client = Client(**data.model_dump())
    try:
        db.add(client)
        db.commit()
        db.refresh(client)
        return client
    except Exception:
        db.rollback()
        raise

@router.patch("/{client_id}", response_model=ClientResponse)
def update_client(client_id: PositiveID, data: ClientUpdate, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    client = db.get(Client, client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    for field, value in data.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(client, field, value)
    try:
        db.add(client)
        db.commit()
        db.refresh(client)
        return client
    except Exception:
        db.rollback()
        raise

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: PositiveID, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    client = db.get(Client, client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    try:
        db.delete(client)
        db.commit()
    except Exception:
        db.rollback()
        raise
