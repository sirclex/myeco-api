from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from schemas.message import Message
from logic import category_logic
from api.deps import get_db

router = APIRouter()

@router.get("", response_model=List[CategoryResponse])
def get_all_categories(db: Session = Depends(get_db)) -> Any:
    return category_logic.get_all_identity_types(db)

@router.post("", response_model=CategoryResponse)
def create_category(*, db: Session = Depends(get_db), wallet_in: CategoryCreate) -> Any:
    return category_logic.create_identity_type(db, wallet_in)

@router.put("", response_model=CategoryResponse)
def update_category(*, db: Session = Depends(get_db), wallet_in: CategoryUpdate) -> Any:
    return category_logic.update_identity_type(db, wallet_in)

@router.delete("", response_model=Message)
def delete_category(*, db: Session = Depends(get_db), id: int) -> Any:
    return category_logic.delete_identity_type(db, id)