from typing import Any

from fastapi import HTTPException, status

from schemas.subcategory import SubcategoryCreate, SubcategoryUpdate
import crud
from sqlalchemy.orm import Session

def get_all_subcategories(db: Session) -> Any:
    subcategories = crud.subcategory.get_multi(db)
    return subcategories

def get_subcategory(db: Session, subcategory_id: int) -> Any:
    subcategory = crud.subcategory.get(db, subcategory_id)
    if not subcategory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The subcategory with this ID does not exist in the system."
        )
    return subcategory

def create_subcategory(db: Session, subcategory_in: SubcategoryCreate) -> Any:
    subcategory = crud.subcategory.create(db, obj_in=subcategory_in)
    return subcategory

def update_subcategory(db: Session, subcategory_in: SubcategoryUpdate) -> Any:
    subcategory = crud.subcategory.get(db, subcategory_in.id)
    if not subcategory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The subcategory with this ID does not exist in the system."
        )
    subcategory = crud.subcategory.update(db, db_obj=subcategory, obj_in=subcategory_in)
    return subcategory

def delete_subcategory(db: Session, subcategory_id: int) -> Any:
    subcategory = crud.subcategory.get(db, subcategory_id)
    if not subcategory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The subcategory with this ID does not exist in the system."
        )
    crud.subcategory.delete(db, model_id=subcategory.id)
    return {"message": f"Subcategory with ID = {id} deleted."}