from typing import Any

from fastapi import HTTPException, status

from schemas.category import CategoryCreate, CategoryUpdate
import crud
from sqlalchemy.orm import Session
from utils.kafka import send_to_kafka
from constants import kafka_topics, exceptions

def get_all_categories(db: Session) -> Any:
    categories = crud.category.get_multi(db)
    return categories


def get_category(db: Session, category_id: int) -> Any:
    category = crud.category.get(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exceptions.CATEGORY_NOT_FOUND,
        )
    return category


def create_category(db: Session, category_in: CategoryCreate) -> Any:
    category = crud.category.create(db, obj_in=category_in)
    send_to_kafka(
        kafka_topics.CATEGORY_CREATE,
        {"id": category.id, "name": category.name},
    )
    return category


def update_category(db: Session, category_in: CategoryUpdate) -> Any:
    category = crud.category.get(db, category_in.id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exceptions.CATEGORY_NOT_FOUND,
        )
    category = crud.category.update(db, db_obj=category, obj_in=category_in)
    send_to_kafka(
        kafka_topics.CATEGORY_UPDATE,
        {"id": category.id, "name": category.name},
    )
    return category


def delete_category(db: Session, category_id: int) -> Any:
    category = crud.category.get(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exceptions.CATEGORY_NOT_FOUND,
        )
    crud.category.delete(db, model_id=category.id)
    return {"message": f"Category with ID = {id} deleted."}
