from typing import Any, List

from fastapi import APIRouter, Depends, Security, HTTPException, status
from sqlalchemy.orm import Session

from schemas.wallet import WalletCreate, WalletUpdate, WalletResponse
from schemas.message import Message
import crud
from logic import wallet_logic
from api.deps import get_db

router = APIRouter()

@router.get("", response_model=List[WalletResponse])
def get_all_wallets(db: Session = Depends(get_db)) -> Any:
    return wallet_logic.get_all_wallets(db)

@router.post("", response_model=WalletResponse)
def create_wallet(*, db: Session = Depends(get_db), wallet_in: WalletCreate) -> Any:
    return wallet_logic.create_wallet(db, wallet_in)

@router.put("", response_model=WalletResponse)
def update_wallet(*, db: Session = Depends(get_db), wallet_in: WalletUpdate) -> Any:
    return wallet_logic.update_wallet(db, wallet_in)

@router.delete("", response_model=Message)
def delete_wallet(*, db: Session = Depends(get_db), id: int) -> Any:
    return wallet_logic.delete_wallet(db, id)