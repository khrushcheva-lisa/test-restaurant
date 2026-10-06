from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.schemas.order import OrderResponse
from app.models.order import Order
from app.database.database import get_db
from app.models.client import Client
from app.schemas.client import *


router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)


@router.get("/", response_model=list[ClientResponse])
def get_clients(db: Session = Depends(get_db)):
    return db.exec(select(Client)).all()


@router.get("/{client_id}", response_model=ClientResponse)
def get_client_by_id(client_id: int, db: Session = Depends(get_db)):
    """Выводит клиента по его идентификатору"""
    client = db.get(Client, client_id)

    if not client:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    return client


@router.get("/client/{client_id}/orders", response_model=list[OrderResponse])
def get_client_all_orders(client_id: int, db: Session = Depends(get_db)):
    """Выводит заказы клиента по его идентификатору"""

    client = db.get(Client, client_id)

    if not client:
            raise HTTPException(
                status_code=404,
                detail="Client not found"
            )
    

    orders = db.exec(
        select(Order).where(Order.client_id == client_id)
    ).all()

    return orders


@router.post("/", response_model=ClientResponse)
def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db)
):
    new_client = Client(
        first_name=client.first_name,
        last_name=client.last_name,
        patronymic=client.patronymic,
        email=client.email,
        phone=client.phone
    )

    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    return new_client


@router.patch("/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, client_data: ClientUpdate, db: Session = Depends(get_db)):
    """Частично изменяет клиента"""
    client = db.get(Client, client_id)

    if not client:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    if client_data.first_name is not None:
        client.first_name = client_data.first_name

    if client_data.last_name is not None:
        client.last_name = client_data.last_name

    if client_data.patronymic is not None:
        client.patronymic = client_data.patronymic

    if client_data.email is not None:
        client.email = client_data.email

    if client_data.phone is not None:
        client.phone = client_data.phone

    db.commit()
    db.refresh(client)

    return client


@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    """Удаляет клиента"""
    client = db.get(Client, client_id)

    if not client:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    db.delete(client)
    db.commit()

    return {"message": "Client deleted successfully"}