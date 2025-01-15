from typing import Any

from fastapi import HTTPException, status

from schemas.transaction import TransactionCreate, TransactionUpdate
from schemas.debt import DebtCreate
import crud
from logic import debt_logic
from sqlalchemy.orm import Session
from utils.kafka import send_to_kafka
from constants import kafka_topics, exceptions


def get_transactions_info(offset: int, limit: int, db: Session) -> Any:
    transactions = crud.transaction.get_transaction_info(db, offset, limit)
    return transactions


def get_transaction(db: Session, transaction_id: int) -> Any:
    transaction = crud.transaction.get(db, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exceptions.TRANSACTION_NOT_FOUND,
        )
    return transaction


def create_transaction(
    db: Session, transaction_in: TransactionCreate, debts_in: list[DebtCreate]
) -> Any:
    transaction = crud.transaction.create(db, obj_in=transaction_in)
    send_to_kafka(
        kafka_topics.TRANSACTION_CREATE,
        {
            "id": transaction.id,
            "issue_at": transaction.issue_at.isoformat(),
            "wallet_id": transaction.wallet_id,
            "is_income": transaction.is_income,
            "amount": transaction.amount,
            "category_id": transaction.category_id,
            "subcategory_id": transaction.subcategory_id,
            "detail": transaction.detail,
            "status_id": transaction.status_id,
        },
    )
    if debts_in:
        for debt_in in debts_in:
            debt_in.transaction_id = transaction.id
            debt_logic.create_debt(db, debt_in)
    return transaction


def update_transaction(db: Session, transaction_in: TransactionUpdate) -> Any:
    transaction = crud.transaction.get(db, transaction_in.id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exceptions.TRANSACTION_NOT_FOUND,
        )
    transaction = crud.transaction.update(db, db_obj=transaction, obj_in=transaction_in)
    send_to_kafka(
        kafka_topics.TRANSACTION_UPDATE,
        {
            "id": transaction.id,
            "issue_at": transaction.issue_at.isoformat(),
            "wallet_id": transaction.wallet_id,
            "is_income": transaction.is_income,
            "amount": transaction.amount,
            "category_id": transaction.category_id,
            "subcategory_id": transaction.subcategory_id,
            "detail": transaction.detail,
            "status_id": transaction.status_id,
        },
    )
    return transaction


def delete_transaction(db: Session, transaction_id: int) -> Any:
    transaction = crud.transaction.get(db, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exceptions.TRANSACTION_NOT_FOUND,
        )
    crud.transaction.delete(db, model_id=transaction.id)
    return {"message": f"Transaction with ID = {id} deleted."}
