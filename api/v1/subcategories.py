from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.subcategory import SubcategoryCreate, SubcategoryUpdate, SubcategoryResponse
from schemas.message import Message
from logic import subcategory_logic
from api.deps import get_db

router = APIRouter()

@router.get("", response_model=List[SubcategoryResponse])
def get_subcategories(db: Session = Depends(get_db), category_id: int = None) -> Any:
    if category_id is not None:
        return subcategory_logic.get_subcategories_by_category_id(db, category_id)
    return subcategory_logic.get_all_subcategories(db)

@router.post("", response_model=SubcategoryResponse)
def create_subcategory(*, db: Session = Depends(get_db), wallet_in: SubcategoryCreate) -> Any:
    return subcategory_logic.create_subcategory(db, wallet_in)

@router.put("", response_model=SubcategoryResponse)
def update_subcategory(*, db: Session = Depends(get_db), wallet_in: SubcategoryUpdate) -> Any:
    return subcategory_logic.update_subcategory(db, wallet_in)

@router.delete("", response_model=Message)
def delete_subcategory(*, db: Session = Depends(get_db), id: int) -> Any:
    return subcategory_logic.delete_subcategory(db, id)