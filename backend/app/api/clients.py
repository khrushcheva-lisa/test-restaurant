from fastapi import APIRouter, Depends
from sqlmodel import Session, select

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