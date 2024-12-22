from typing import Any

from fastapi import HTTPException, status

from schemas.identity import IdentityCreate, IdentityUpdate
import crud
from sqlalchemy.orm import Session

def get_all_identities(db: Session) -> Any:
    identities = crud.identity.get_multi(db)
    return identities

def get_identity(db: Session, identity_id: int) -> Any:
    identity = crud.identity.get(db, identity_id)
    if not identity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The identity with this ID does not exist in the system."
        )
    return identity

def create_identity(db: Session, identity_in: IdentityCreate) -> Any:
    identity_type = crud.identity_type.get(db, identity_in.type_id)
    if not identity_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The identity type with this ID does not exist in the system."
        )
    identity = crud.identity.create(db, obj_in=identity_in)
    return identity

def update_identity(db: Session, identity_in: IdentityUpdate) -> Any:
    identity = crud.identity.get(db, identity_in.id)
    if not identity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The identity with this ID does not exist in the system."
        )
    identity = crud.identity.update(db, db_obj=identity, obj_in=identity_in)
    return identity

def delete_identity(db: Session, identity_id: int) -> Any:
    identity = crud.identity.get(db, identity_id)
    if not identity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The identity with this ID does not exist in the system."
        )
    crud.identity.delete(db, model_id=identity.id)
    return {"message": f"Identity with ID = {id} deleted."}