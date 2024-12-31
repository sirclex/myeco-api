from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class WalletBase(BaseModel):
    name: Optional[str]
    provider: Optional[str]
    number: Optional[str]
    balance: Optional[float]

class WalletCreate(WalletBase):
    name: str
    provider: str
    balance: float
    updated_at: Optional[datetime] = datetime.now()
    logical_delete: bool = False

class WalletUpdate(WalletBase):
    id: int
    updated_at: Optional[datetime] = datetime.now()

class WalletDelete(WalletBase):
    id: int
    updated_at: Optional[datetime] = datetime.now()
    logical_delete: bool = True

class WalletResponse(WalletBase):
    id: Optional[int]
    class Config:
        from_attributes = True