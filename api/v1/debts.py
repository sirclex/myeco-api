from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.debt import DebtCreate, DebtUpdate, DebtResponse
from schemas.message import Message
from logic import debt_logic
from api.deps import get_db

router = APIRouter()

@router.get("", response_model=List[DebtResponse])
def get_all_debts(db: Session = Depends(get_db)) -> Any:
    return debt_logic.get_all_debts_info(db)

@router.post("", response_model=DebtResponse)
def create_debt(*, db: Session = Depends(get_db), wallet_in: DebtCreate) -> Any:
    return debt_logic.create_debt(db, wallet_in)

@router.put("", response_model=DebtResponse)
def update_debt(*, db: Session = Depends(get_db), wallet_in: DebtUpdate) -> Any:
    return debt_logic.update_debt(db, wallet_in)

@router.put("/multi", response_model=List[DebtResponse])
def update_multi_debts(*, db: Session = Depends(get_db), debts_in: list[DebtUpdate]) -> Any:
    return debt_logic.update_multi_debts(db, debts_in)

@router.delete("", response_model=Message)
def delete_debt(*, db: Session = Depends(get_db), id: int) -> Any:
    return debt_logic.delete_debt(db, id)