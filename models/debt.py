from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel

from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import func


from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from models.base import Base
from models.identity import IdentityModel
from models.transaction_status import TransactionStatusModel

class Debt(Base):
    __tablename__ = "Debt"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    transaction_id: Mapped[int] = mapped_column(ForeignKey("Transaction.id"))
    transaction: Mapped["Transaction"] = relationship(back_populates="debts")
    in_out: Mapped[bool] = mapped_column(Boolean)
    amount: Mapped[float] = mapped_column(Float)
    identity_id: Mapped[int] = mapped_column(ForeignKey("Identity.id"))
    identity: Mapped["Identity"] = relationship(back_populates="debts")
    detail: Mapped[str] = mapped_column(String(128))
    status_id: Mapped[int] = mapped_column(ForeignKey("TransactionStatus.id"))
    status: Mapped["TransactionStatus"] = relationship(back_populates="debts")
    created_at: Mapped[datetime] = mapped_column(server_default=func.CURRENT_TIMESTAMP())
    updated_at: Mapped[datetime] = mapped_column(DateTime)
    logical_delete: Mapped[bool] = mapped_column(Boolean)

class DebtModel(BaseModel):
    id: Optional[int] = None
    transaction_id: Optional[int] = None
    in_out: Optional[bool] = None
    amount: Optional[float] = None
    identity_id: Optional[int] = None
    identity: Optional[IdentityModel] = None
    detail: Optional[str] = None
    status_id: Optional[int] = None
    status: Optional[TransactionStatusModel] = None
    updated_at: Optional[datetime] = datetime.now()
    logical_delete: Optional[bool] = False