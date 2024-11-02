from datetime import datetime

from sqlalchemy import insert, select, update, func, and_

from sqlalchemy.orm import Session

from typing import List

from models.debt import Debt, DebtModel
from models.identity import Identity, IdentityModel
from models.identity_type import IdentityTypeModel
from models.transaction_status import TransactionStatusModel

def create_debt(debt: DebtModel, engine):
    session = Session(engine)
    result = session.execute(
        insert(Debt).returning(Debt.id),
        [
            {
                "transaction_id": debt.transaction_id,
                "in_out": debt.in_out,
                "amount": debt.amount,
                "identity_id": debt.identity_id,
                "detail": debt.detail,
                "status_id": debt.status_id,
                "updated_at": datetime.now(),
                "logical_delete": False
            }
        ]
    ).first()
    session.commit()
    session.close()
    return result[0]

def create_multiple_debt(debts: List[DebtModel], engine):
    session = Session(engine)
    session.execute(
        insert(Debt),debts
    )
    session.commit()
    session.close()
    return 1

def get_all_debts(engine):
    session = Session(engine)
    result = session.execute(
        select(Debt)
        .where(Debt.logical_delete == False)
    )
    results = []
    for row in result:
        results.append(DebtModel(
            id = row[0].id,
            transaction_id = row[0].transaction_id,
            in_out = row[0].in_out,
            amount = row[0].amount,
            identity_id = row[0].identity.id,
            identity = IdentityModel(
                id = row[0].identity.id,
                name = row[0].identity.name,
                type_id = row[0].identity.type.id,
                type = IdentityTypeModel(
                    id = row[0].identity.type.id,
                    name = row[0].identity.type.name
                )
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

def get_sum_debt_by_identity(engine):
    stmt = select(
        Identity.name,
        Debt.in_out,
        func.sum(Debt.amount).label("amount")
    ).join(
        Identity, 
        Debt.identity_id == Identity.id
    ).where(
        Debt.status_id == 1
    ).group_by(Identity.name, Debt.in_out)
    session = Session(engine)
    result = session.execute(stmt).fetchall()
    return result

def get_debt(id, engine):
    session = Session(engine)
    row = session.execute(
        select(Debt)
        .where(Debt.id == id)
        .where(Debt.logical_delete == False)
    ).first()
    if (row != None):
        result = DebtModel(
            id = row[0].id,
            transaction_id = row[0].transaction_id,
            in_out = row[0].in_out,
            amount = row[0].amount,
            identity_id = row[0].identity.id,
            identity = IdentityModel(
                id = row[0].identity.id,
                name = row[0].identity.name,
                type_id = row[0].identity.type.id,
                type = IdentityTypeModel(
                    id = row[0].identity.type.id,
                    name = row[0].identity.type.name
                )
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

def update_debt(debt: DebtModel, engine):
    session = Session(engine)
    result = session.execute(
        update(Debt)
        .where(Debt.id == debt.id)
        .values(
            transaction_id=debt.transaction_id,
            in_out=debt.in_out,
            amount=debt.amount,
            identity_id=debt.identity_id,
            detail=debt.detail,
            status_id=debt.status_id,
            updated_at=datetime.now()
        )
    )
    session.commit()
    session.close()
    return result.rowcount

def revive_debt(id, engine):
    session = Session(engine)
    results = session.execute(
        update(Debt)
        .where(Debt.id == id)
        .values(updated_at=datetime.now(), logical_delete = False)
    )
    session.commit()
    session.close()
    return results.rowcount

def delete_debt(id, engine):
    session = Session(engine)
    results = session.execute(
        update(Debt)
        .where(Debt.id == id)
        .values(updated_at=datetime.now(), logical_delete = True)
    )
    session.commit()
    session.close()
    return results.rowcount