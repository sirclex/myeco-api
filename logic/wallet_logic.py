from typing import Any

from fastapi import HTTPException, status

from schemas.wallet import WalletCreate, WalletUpdate
import crud
from sqlalchemy.orm import Session
from utils.kafka import send_to_kafka
from constants import kafka_topics, exceptions

def get_all_wallets(db: Session) -> Any:
    wallets = crud.wallet.get_multi(db)
    return wallets


def create_wallet(db: Session, wallet_in: WalletCreate) -> Any:
    wallet = crud.wallet.create(db, obj_in=wallet_in)
    send_to_kafka(
        kafka_topics.WALLET_CREATE,
        {
            "id": wallet.id,
            "name": wallet.name,
            "provider": wallet.provider,
            "number": wallet.number,
        },
    )
    return wallet


def update_wallet(db: Session, wallet_in: WalletUpdate) -> Any:
    wallet = crud.wallet.get(db, wallet_in.id)
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exceptions.WALLET_NOT_FOUND,
        )
    wallet = crud.wallet.update(db, db_obj=wallet, obj_in=wallet_in)
    send_to_kafka(
        kafka_topics.WALLET_UPDATE,
        {
            "id": wallet.id,
            "name": wallet.name,
            "provider": wallet.provider,
            "number": wallet.number,
        },
    )
    return wallet


def delete_wallet(db: Session, wallet_id: int) -> Any:
    wallet = crud.wallet.get(db, wallet_id)
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exceptions.WALLET_NOT_FOUND,
        )
    crud.wallet.delete(db, model_id=wallet.id)
    return {"message": f"Product with ID = {id} deleted."}
