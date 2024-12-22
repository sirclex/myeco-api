from typing import Any

from fastapi import HTTPException, status

from schemas.debt import DebtCreate, DebtUpdate
import crud
from sqlalchemy.orm import Session

def get_all_debts(db: Session) -> Any:
    debts = crud.debt.get_multi(db)
    return debts

def get_debt(db: Session, debt_id: int) -> Any:
    debt = crud.debt.get(db, debt_id)
    if not debt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The debt with this ID does not exist in the system."
        )
    return debt

def create_debt(db: Session, debt_in: DebtCreate) -> Any:
    debt = crud.debt.create(db, obj_in=debt_in)
    return debt

def update_debt(db: Session, debt_in: DebtUpdate) -> Any:
    debt = crud.debt.get(db, debt_in.id)
    if not debt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The debt with this ID does not exist in the system."
        )
    debt = crud.debt.update(db, db_obj=debt, obj_in=debt_in)
    return debt

def delete_debt(db: Session, debt_id: int) -> Any:
    debt = crud.debt.get(db, debt_id)
    if not debt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The debt with this ID does not exist in the system."
        )
    crud.debt.delete(db, model_id=debt.id)
    return {"message": f"Debt with ID = {id} deleted."}