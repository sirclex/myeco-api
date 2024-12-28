from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class TransactionBase(BaseModel):
    issue_at: Optional[datetime] = None
    wallet_id: Optional[int] = None
    is_income: Optional[bool] = None
    amount: Optional[float] = None
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    detail: Optional[str] = None
    status_id: Optional[int] = None

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
    wallet: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    status: Optional[str] = None
    class Config:
        from_attributes = True