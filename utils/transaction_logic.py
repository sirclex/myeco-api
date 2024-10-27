from datetime import datetime

from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update

from sqlalchemy.orm import Session

from typing import List

from models.transaction import Transaction, TransactionModel
from models.wallet import Wallet, WalletModel
from models.transaction_category import TransactionCategory, TransactionCategoryModel
from models.transaction_subcategory import TransactionSubcategory, TransactionSubcategoryModel
from models.transaction_status import TransactionStatusModel
from models.debt import DebtModel

def create_transaction(transaction: TransactionModel, engine):
    statement = insert(Transaction).values(
        issue_date=transaction.issue_date,
        wallet_id=transaction.wallet_id,
        in_out=transaction.in_out,
        amount=transaction.amount,
        category_id=transaction.category_id,
        subcategory_id=transaction.subcategory_id,
        detail=transaction.detail,
        status_id=transaction.status_id,
        updated_at=datetime.now(),
        logical_delete=False
    ).returning(Transaction.id)
    session = Session(engine)
    result = session.execute(statement).scalars().first()
    session.commit()
    return result

def create_transaction_with_debts(transaction: TransactionModel, debts: List[DebtModel], engine):
    statement = insert(Transaction).values(
        issue_date=transaction.issue_date,
        wallet_id=transaction.wallet_id,
        in_out=transaction.in_out,
        amount=transaction.amount,
        category_id=transaction.category_id,
        subcategory_id=transaction.subcategory_id,
        detail=transaction.detail,
        status_id=transaction.status_id,
        updated_at=datetime.now(),
        logical_delete=False
    ).returning(Transaction.id)
    session = Session(engine)
    result = session.execute(statement).scalars().first()
    session.commit()
    return result

def get_all_transactions(engine):
    session = Session(engine)
    statement = select(Transaction).where(Transaction.logical_delete == False)
    result = session.execute(statement)
    results = []
    for row in result:
        results.append(TransactionModel(
            id = row[0].id,
            issue_date = row[0].issue_date,
            wallet_id = row[0].wallet.id,
            wallet = WalletModel(
                id = row[0].wallet.id,
                name = row[0].wallet.name,
                provider = row[0].wallet.provider,
                number = row[0].wallet.number,
                balance = row[0].wallet.balance
            ),
            in_out = row[0].in_out,
            amount = row[0].amount,
            category_id = row[0].category.id,
            category = TransactionCategoryModel(
                id = row[0].category.id,
                name = row[0].category.name
            ),
            subcategory_id=row[0].subcategory.id,
            subcategory=TransactionSubcategoryModel(
                id = row[0].subcategory.id,
                name = row[0].subcategory.name,
                transaction_category_id = row[0].subcategory.transaction_category_id
            ),
            detail=row[0].detail,
            status_id=row[0].status.id,
            status=TransactionStatusModel(
                id = row[0].status.id,
                name = row[0].status.name
            )
        ))
    session.close()
    return results

def get_transaction(id, engine):
    session = Session(engine)
    row = session.execute(
        select(Transaction)
        .where(Transaction.id == id)
        .where(Transaction.logical_delete == False)
    ).first()
    if (row != None):
        result = TransactionModel(
            id = row[0].id,
            issue_date = row[0].issue_date,
            wallet_id = row[0].wallet.id,
            wallet = WalletModel(
                id = row[0].wallet.id,
                name = row[0].wallet.name,
                provider = row[0].wallet.provider,
                number = row[0].wallet.number,
                balance = row[0].wallet.balance
            ),
            in_out = row[0].in_out,
            amount = row[0].amount,
            category_id = row[0].category.id,
            category = TransactionCategoryModel(
                id = row[0].category.id,
                name = row[0].category.name
            ),
            subcategory_id=row[0].subcategory.id,
            subcategory=TransactionSubcategoryModel(
                id = row[0].subcategory.id,
                name = row[0].subcategory.name,
                transaction_category_id = row[0].subcategory.transaction_category_id
            ),
            detail=row[0].detail,
            status_id=row[0].status.id,
            status=TransactionStatusModel(
                id = row[0].status.id,
                name = row[0].status.name
            )
        )
        return result
    session.close()

def update_transaction(transaction: TransactionModel, engine):
    session = Session(engine)
    result = session.execute(
        update(Transaction)
        .where(Transaction.id == transaction.id)
        .values(
            issue_date=transaction.name,
            wallet_id=transaction.wallet_id,
            in_out=transaction.in_out,
            amount=transaction.amount,
            category_id=transaction.category_id,
            subcategory_id=transaction.subcategory_id,
            detail=transaction.detail,
            status_id=transaction.status_id,
            updated_at=datetime.now()
        )
    )
    session.commit()
    session.close()
    return result.rowcount

def revive_transaction(id, engine):
    session = Session(engine)
    results = session.execute(
        update(Transaction)
        .where(Transaction.id == id)
        .values(updated_at=datetime.now(), logical_delete = False)
    )
    session.commit()
    session.close()
    return results.rowcount

def delete_transaction(id, engine):
    session = Session(engine)
    results = session.execute(
        update(Transaction)
        .where(Transaction.id == id)
        .values(updated_at=datetime.now(), logical_delete = True)
    )
    session.commit()
    session.close()
    return results.rowcount