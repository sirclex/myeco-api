from typing import Any

from fastapi import HTTPException, status

from schemas.debt import DebtCreate, DebtUpdate
from schemas.transaction import TransactionUpdate
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

def update_multi_debts(db: Session, debts_in: list[DebtUpdate]) -> Any:
    debts = crud.debt.update_multi(db, objs_in=debts_in)
    
    transaction_ids_pending = []
    transaction_ids_done = []

    print(debts)

    for debt in debts:
        if debt.status_id == 1:
            transaction_ids_pending.append(debt.transaction_id)
        elif debt.status_id == 2:
            transaction_ids_done.append(debt.transaction_id)

    transaction_ids_pending = list(set(transaction_ids_pending))
    transaction_ids_done = list(set(transaction_ids_done) - set(transaction_ids_pending))

    transaction_models = []
    for transaction_id in transaction_ids_pending:
        transaction_models.append(
            TransactionUpdate(id=transaction_id, status_id=1)
        )
    
    for transaction_id in transaction_ids_done:
        transaction_models.append(
            TransactionUpdate(id=transaction_id, status_id=2)
        )

    crud.transaction.update_multi(db, objs_in=transaction_models)

    return debts

def delete_debt(db: Session, debt_id: int) -> Any:
    debt = crud.debt.get(db, debt_id)
    if not debt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The debt with this ID does not exist in the system."
        )
    crud.debt.delete(db, model_id=debt.id)
    return {"message": f"Debt with ID = {id} deleted."}