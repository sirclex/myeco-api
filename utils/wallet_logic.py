from datetime import datetime

from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
# from sqlalchemy import delete

from sqlalchemy.orm import Session

from models.wallet import Wallet, WalletModel

def create_wallet(wallet: WalletModel, engine):
    session = Session(engine)
    result = session.execute(
        insert(Wallet),
        [
            {
                "name": wallet.name,
                "provider": wallet.provider,
                "number": wallet.number,
                "balance": wallet.balance,
                "updated_at": datetime.now(),
                "logical_delete": False
            }
        ]
    )
    session.commit()
    session.close()
    return result

def get_all_wallets(engine):
    session = Session(engine)
    result = session.execute(
        select(Wallet)
        .where(Wallet.logical_delete == False)
    )
    results = []
    for row in result:
        results.append(WalletModel(
            id=row[0].id,
            name=row[0].name,
            provider=row[0].provider,
            number=row[0].number,
            balance=row[0].balance
        ))
    session.close()
    return results

def get_wallet(id, engine):
    session = Session(engine)
    row = session.execute(
        select(Wallet)
        .where(Wallet.id == id)
        .where(Wallet.logical_delete == False)
    ).first()
    if (row != None):
        result = WalletModel(
            id=row[0].id,
            name=row[0].name,
            provider=row[0].provider,
            number=row[0].number,
            balance=row[0].balance
        )
        return result
    session.close()

def update_wallet(wallet: WalletModel, engine):
    session = Session(engine)
    result = session.execute(
        update(Wallet)
        .where(Wallet.id == wallet.id)
        .values(
            name=wallet.name,
            provider=wallet.provider,
            number=wallet.number,
            balance=wallet.balance,
            updated_at=datetime.now()
        )
    )
    session.commit()
    session.close()
    return result.rowcount

def revive_wallet(id, engine):
    session = Session(engine)
    results = session.execute(
        update(Wallet)
        .where(Wallet.id == id)
        .values(updated_at=datetime.now(), logical_delete = False)
    )
    session.commit()
    session.close()
    return results.rowcount

def delete_wallet(id, engine):
    session = Session(engine)
    results = session.execute(
        update(Wallet)
        .where(Wallet.id == id)
        .values(updated_at=datetime.now(), logical_delete = True)
    )
    session.commit()
    session.close()
    return results.rowcount