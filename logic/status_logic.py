from typing import Any

import fastapi
from fastapi import HTTPException

from schemas.status import StatusCreate, StatusUpdate
import crud
from sqlalchemy.orm import Session

def get_all_statuses(db: Session) -> Any:
    statuses = crud.status.get_multi(db)
    return statuses

def get_status(db: Session, status_id: int) -> Any:
    status = crud.status.get(db, status_id)
    if not status:
        raise HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="The status with this ID does not exist in the system."
        )
    return status

def create_status(db: Session, status_in: StatusCreate) -> Any:
    status = crud.status.create(db, obj_in=status_in)
    return status

def update_status(db: Session, status_in: StatusUpdate) -> Any:
    status = crud.status.get(db, status_in.id)
    if not status:
        raise HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="The status with this ID does not exist in the system."
        )
    status = crud.status.update(db, db_obj=status, obj_in=status_in)
    return status

def delete_status(db: Session, status_id: int) -> Any:
    status = crud.status.get(db, status_id)
    if not status:
        raise HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="The status with this ID does not exist in the system."
        )
    crud.status.delete(db, model_id=status.id)
    return {"message": f"Status with ID = {id} deleted."}