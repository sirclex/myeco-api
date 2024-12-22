from typing import Any

from fastapi import HTTPException, status

from schemas.transaction import TransactionCreate, TransactionUpdate
from schemas.debt import DebtCreate
import crud
from sqlalchemy.orm import Session

def get_all_transactions(db: Session) -> Any:
    transactions = crud.transaction.get_multi(db)
    return transactions

def get_transaction(db: Session, transaction_id: int) -> Any:
    transaction = crud.transaction.get(db, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The transaction with this ID does not exist in the system."
        )
    return transaction

def create_transaction(db: Session, transaction_in: TransactionCreate, debts_in: list[DebtCreate]) -> Any:
    transaction = crud.transaction.create(db, obj_in=transaction_in)
    if (debts_in):
        for debt_in in debts_in:
            debt_in.transaction_id = transaction.id
            crud.debt.create(db, obj_in=debt_in)
    return transaction

def update_transaction(db: Session, transaction_in: TransactionUpdate) -> Any:
    transaction = crud.transaction.get(db, transaction_in.id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The transaction with this ID does not exist in the system."
        )
    transaction = crud.transaction.update(db, db_obj=transaction, obj_in=transaction_in)
    return transaction

def delete_transaction(db: Session, transaction_id: int) -> Any:
    transaction = crud.transaction.get(db, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The transaction with this ID does not exist in the system."
        )
    crud.transaction.delete(db, model_id=transaction.id)
    return {"message": f"Transaction with ID = {id} deleted."}