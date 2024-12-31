from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class IdentityTypeBase(BaseModel):
    name: Optional[str]

class IdentityTypeCreate(IdentityTypeBase):
    name: str
    updated_at: Optional[datetime] = datetime.now()
    logical_delete: bool = False

class IdentityTypeUpdate(IdentityTypeBase):
    id: int
    updated_at: Optional[datetime] = datetime.now()

class IdentityTypeDelete(IdentityTypeBase):
    id: int
    updated_at: Optional[datetime] = datetime.now()
    logical_delete: bool = True

class IdentityTypeResponse(IdentityTypeBase):
    id: Optional[int]
    class Config:
        from_attributes = True