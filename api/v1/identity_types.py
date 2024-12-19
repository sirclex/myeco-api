from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.identity_type import IdentityTypeCreate, IdentityTypeUpdate, IdentityTypeResponse
from schemas.message import Message
from logic import identity_type_logic
from api.deps import get_db

router = APIRouter()

@router.get("", response_model=List[IdentityTypeResponse])
def get_all_identity_types(db: Session = Depends(get_db)) -> Any:
    return identity_type_logic.get_all_identity_types(db)

@router.post("", response_model=IdentityTypeResponse)
def create_identity_type(*, db: Session = Depends(get_db), wallet_in: IdentityTypeCreate) -> Any:
    return identity_type_logic.create_identity_type(db, wallet_in)

@router.put("", response_model=IdentityTypeResponse)
def update_identity_type(*, db: Session = Depends(get_db), wallet_in: IdentityTypeUpdate) -> Any:
    return identity_type_logic.update_identity_type(db, wallet_in)

@router.delete("", response_model=Message)
def delete_identity_type(*, db: Session = Depends(get_db), id: int) -> Any:
    return identity_type_logic.delete_identity_type(db, id)