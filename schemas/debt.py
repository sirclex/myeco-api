from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class DebtBase(BaseModel):
    transaction_id: Optional[int]
    is_income: Optional[bool]
    amount: Optional[float]
    identity_id: Optional[int]
    detail: Optional[str]
    status_id: Optional[int]

class DebtCreate(DebtBase):
    transaction_id: Optional[int] = None
    is_income: bool
    amount: float
    identity_id: int
    detail: str
    status_id: int
    updated_at: datetime = datetime.now()
    logical_delete: bool = False

class DebtUpdate(DebtBase):
    id: int
    updated_at: datetime = datetime.now()

class DebtDelete(DebtBase):
    id: int
    updated_at: datetime = datetime.now()
    logical_delete: bool = True

class DebtResponse(DebtBase):
    id: Optional[int]
    class Config:
        from_attributes = True