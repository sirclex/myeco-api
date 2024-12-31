from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class IdentityBase(BaseModel):
    name: Optional[str]
    type_id: Optional[int]

class IdentityCreate(IdentityBase):
    name: str
    type_id: int
    updated_at: Optional[datetime] = datetime.now()
    logical_delete: bool = False

class IdentityUpdate(IdentityBase):
    id: int
    updated_at: Optional[datetime] = datetime.now()

class IdentityDelete(IdentityBase):
    id: int
    updated_at: Optional[datetime] = datetime.now()
    logical_delete: bool = True

class IdentityResponse(IdentityBase):
    id: Optional[int]
    class Config:
        from_attributes = True