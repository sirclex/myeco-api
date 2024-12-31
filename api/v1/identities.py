from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.identity import IdentityCreate, IdentityUpdate, IdentityResponse
from schemas.message import Message
from logic import identity_logic
from api.deps import get_db

router = APIRouter()

@router.get("", response_model=List[IdentityResponse])
def get_all_identities(db: Session = Depends(get_db)) -> Any:
    return identity_logic.get_all_identities(db)

@router.post("", response_model=IdentityResponse)
def create_identity(*, db: Session = Depends(get_db), wallet_in: IdentityCreate) -> Any:
    return identity_logic.create_identity(db, wallet_in)

@router.put("", response_model=IdentityResponse)
def update_identity(*, db: Session = Depends(get_db), wallet_in: IdentityUpdate) -> Any:
    return identity_logic.update_identity(db, wallet_in)

@router.delete("", response_model=Message)
def delete_identity(*, db: Session = Depends(get_db), id: int) -> Any:
    return identity_logic.delete_identity(db, id)