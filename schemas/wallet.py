from typing import Optional
from pydantic import BaseModel

class WalletBase(BaseModel):
    id: Optional[int]
    name: Optional[str]
    provider: Optional[str]
    number: Optional[str]
    balance: Optional[float]

class WalletCreate(WalletBase):
    id: int = None
    name: str
    provider: str
    balance: float

class WalletUpdate(WalletBase):
    id: int

class WalletResponse(WalletBase):
    class Config:
        from_attributes = True