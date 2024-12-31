from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class StatusBase(BaseModel):
    name: Optional[str]

class StatusCreate(StatusBase):
    name: str
    updated_at: Optional[datetime] = datetime.now()
    logical_delete: bool = False

class StatusUpdate(StatusBase):
    id: int
    updated_at: Optional[datetime] = datetime.now()

class StatusDelete(StatusBase):
    id: int
    updated_at: Optional[datetime] = datetime.now()
    logical_delete: bool = True

class StatusResponse(StatusBase):
    id: Optional[int]
    class Config:
        from_attributes = True