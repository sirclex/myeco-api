from typing import Any

from fastapi import HTTPException, status

from schemas.subcategory import SubcategoryCreate, SubcategoryUpdate
import crud
from sqlalchemy.orm import Session
from utils.kafka import send_to_kafka
from constants import kafka_topics, exceptions

def get_all_subcategories(db: Session) -> Any:
    subcategories = crud.subcategory.get_multi(db)
    return subcategories


def get_subcategories_by_category_id(db: Session, category_id: int) -> Any:
    subcategories = crud.subcategory.get_by_category_id(db, category_id)
    return subcategories


def get_subcategory(db: Session, subcategory_id: int) -> Any:
    subcategory = crud.subcategory.get(db, subcategory_id)
    if not subcategory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exceptions.SUBCATEGORY_NOT_FOUND,
        )
    return subcategory


def create_subcategory(db: Session, subcategory_in: SubcategoryCreate) -> Any:
    subcategory = crud.subcategory.create(db, obj_in=subcategory_in)
    send_to_kafka(
        kafka_topics.SUBCATEGORY_CREATE,
        {
            "id": subcategory.id,
            "category_id": subcategory.category_id,
            "name": subcategory.name,
        },
    )
    return subcategory


def update_subcategory(db: Session, subcategory_in: SubcategoryUpdate) -> Any:
    subcategory = crud.subcategory.get(db, subcategory_in.id)
    if not subcategory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exceptions.SUBCATEGORY_NOT_FOUND,
        )
    subcategory = crud.subcategory.update(db, db_obj=subcategory, obj_in=subcategory_in)
    send_to_kafka(
        kafka_topics.SUBCATEGORY_UPDATE,
        {
            "id": subcategory.id,
            "category_id": subcategory.category_id,
            "name": subcategory.name,
        },
    )
    return subcategory


def delete_subcategory(db: Session, subcategory_id: int) -> Any:
    subcategory = crud.subcategory.get(db, subcategory_id)
    if not subcategory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exceptions.SUBCATEGORY_NOT_FOUND,
        )
    crud.subcategory.delete(db, model_id=subcategory.id)
    return {"message": f"Subcategory with ID = {id} deleted."}
