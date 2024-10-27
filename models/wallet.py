from datetime import datetime
from typing import List
from typing import Optional

from fastapi import Query
from pydantic import BaseModel

from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Boolean

from sqlalchemy import func

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from models.base import Base

class Wallet(Base):
    __tablename__ = "Wallet"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32))
    provider: Mapped[str] = mapped_column(String(32))
    number: Mapped[str] = mapped_column(String(128))
    balance: Mapped[float] = mapped_column(Float)
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="wallet")
    created_at: Mapped[datetime] = mapped_column(server_default=func.CURRENT_TIMESTAMP())
    updated_at: Mapped[datetime] = mapped_column(DateTime)
    logical_delete: Mapped[bool] = mapped_column(Boolean)

class WalletModel(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = Query(default=None, min_length=1)
    provider: Optional[str] = None
    number: Optional[str] = None
    balance: Optional[float] = None