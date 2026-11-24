from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.database.database import get_db
from app.core.validation import PositiveID
from app.api.errors import controller_http_error
from app.api.auth_router import manager_or_admin
from app.schemas.employees_schema import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.controllers.employees_controller import EmployeeController

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.get("/", response_model=list[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    try: return EmployeeController.get_all(db)
    except Exception as exc: raise controller_http_error(exc)

@router.get("/waiters", response_model=list[EmployeeResponse])
def get_waiters(db: Session = Depends(get_db)):
    try: return EmployeeController.get_by_position("Официант", db)
    except Exception as exc: raise controller_http_error(exc)

@router.get("/managers", response_model=list[EmployeeResponse])
def get_managers(db: Session = Depends(get_db)):
    try: return EmployeeController.get_by_position("Менеджер", db)
    except Exception as exc: raise controller_http_error(exc)

@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee_by_id(employee_id: PositiveID, db: Session = Depends(get_db)):
    try: return EmployeeController.get_by_id(employee_id, db)
    except Exception as exc: raise controller_http_error(exc)

@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(data: EmployeeCreate, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    try: return EmployeeController.create(data, db)
    except Exception as exc: raise controller_http_error(exc)

@router.patch("/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: PositiveID, data: EmployeeUpdate, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    try: return EmployeeController.update(employee_id, data, db)
    except Exception as exc: raise controller_http_error(exc)

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: PositiveID, db: Session = Depends(get_db), _=Depends(manager_or_admin)):
    try: EmployeeController.delete(employee_id, db); return None
    except Exception as exc: raise controller_http_error(exc)


