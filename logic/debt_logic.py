from typing import Any

from fastapi import HTTPException, status

from schemas.debt import DebtCreate, DebtUpdate
from schemas.transaction import TransactionUpdate
import crud
from sqlalchemy.orm import Session
from utils.kafka import send_to_kafka
from constants import kafka_topics, exceptions

def get_all_debts_info(db: Session) -> Any:
    debts = crud.debt.get_all_debts(db)
    return debts


def get_debt(db: Session, debt_id: int) -> Any:
    debt = crud.debt.get(db, debt_id)
    if not debt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exceptions.DEBT_NOT_FOUND,
        )
    return debt


def create_debt(db: Session, debt_in: DebtCreate) -> Any:
    debt = crud.debt.create(db, obj_in=debt_in)
    send_to_kafka(
        kafka_topics.DEBT_CREATE,
        {
            "id": debt.id,
            "transaction_id": debt.transaction_id,
            "is_income": debt.is_income,
            "amount": debt.amount,
            "identity_id": debt.identity_id,
            "detail": debt.detail,
            "status_id": debt.status_id,
        },
    )
    return debt


def update_debt(db: Session, debt_in: DebtUpdate) -> Any:
    debt = crud.debt.get(db, debt_in.id)
    if not debt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exceptions.DEBT_NOT_FOUND,
        )
    debt = crud.debt.update(db, db_obj=debt, obj_in=debt_in)
    send_to_kafka(
        kafka_topics.DEBT_UPDATE,
        {
            "id": debt.id,
            "transaction_id": debt.transaction_id,
            "is_income": debt.is_income,
            "amount": debt.amount,
            "identity_id": debt.identity_id,
            "detail": debt.detail,
            "status_id": debt.status_id,
        },
    )
    return debt


def update_multi_debts(db: Session, debts_in: list[DebtUpdate]) -> Any:
    debts = crud.debt.update_multi(db, objs_in=debts_in)

    transaction_ids_pending = []
    transaction_ids_done = []

    for debt in debts:
        if debt.status_id == 1:
            transaction_ids_pending.append(debt.transaction_id)
        elif debt.status_id == 2:
            transaction_ids_done.append(debt.transaction_id)

    transaction_ids_pending = list(set(transaction_ids_pending))
    transaction_ids_done = list(
        set(transaction_ids_done) - set(transaction_ids_pending)
    )

    transaction_models = []
    for transaction_id in transaction_ids_pending:
        transaction_models.append(TransactionUpdate(id=transaction_id, status_id=1))

    for transaction_id in transaction_ids_done:
        transaction_models.append(TransactionUpdate(id=transaction_id, status_id=2))

    transactions = crud.transaction.update_multi(db, objs_in=transaction_models)
    cooked_kafka_data = []
    for debt in debts:
        cooked_kafka_data.append(
            {
                "id": debt.id,
                "transaction_id": debt.transaction_id,
                "is_income": debt.is_income,
                "amount": debt.amount,
                "identity_id": debt.identity_id,
                "detail": debt.detail,
                "status_id": debt.status_id,
            }
        )
    send_to_kafka(kafka_topics.DEBT_UPDATE_MULTI, cooked_kafka_data)

    cooked_kafka_data = []
    for transaction in transactions:
        cooked_kafka_data.append(
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
            }
        )
    send_to_kafka(kafka_topics.TRANSACTION_UPDATE_MULTI, cooked_kafka_data)
    return debts


def delete_debt(db: Session, debt_id: int) -> Any:
    debt = crud.debt.get(db, debt_id)
    if not debt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exceptions.DEBT_NOT_FOUND,
        )
    crud.debt.delete(db, model_id=debt.id)
    return {"message": f"Debt with ID = {id} deleted."}
