from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class TransactionBase(BaseModel):
    issue_at: Optional[datetime]
    wallet_id: Optional[int]
    is_income: Optional[bool]
    amount: Optional[float]
    category_id: Optional[int]
    subcategory_id: Optional[int]
    detail: Optional[str]
    status_id: Optional[int]

class TransactionCreate(TransactionBase):
    issue_at: datetime
    wallet_id: int
    is_income: bool
    amount: float
    category_id: int
    subcategory_id: int
    detail: str
    status_id: int
    updated_at: datetime = datetime.now()
    logical_delete: bool = False

class TransactionUpdate(TransactionBase):
    id: int
    updated_at: datetime = datetime.now()

class TransactionDelete(TransactionBase):
    id: int
    updated_at: datetime = datetime.now()
    logical_delete: bool = True

class TransactionResponse(TransactionBase):
    id: Optional[int]
    class Config:
        from_attributes = True