from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.status import StatusCreate, StatusUpdate, StatusResponse
from schemas.message import Message
from logic import status_logic
from api.deps import get_db

router = APIRouter()

@router.get("", response_model=List[StatusResponse])
def get_all_statuses(db: Session = Depends(get_db)) -> Any:
    return status_logic.get_all_statuses(db)

@router.post("", response_model=StatusResponse)
def create_status(*, db: Session = Depends(get_db), status_in: StatusCreate) -> Any:
    return status_logic.create_status(db, status_in)

@router.put("", response_model=StatusResponse)
def update_status(*, db: Session = Depends(get_db), status_in: StatusUpdate) -> Any:
    return status_logic.update_status(db, status_in)

@router.delete("", response_model=Message)
def delete_status(*, db: Session = Depends(get_db), id: int) -> Any:
    return status_logic.delete_status(db, id)