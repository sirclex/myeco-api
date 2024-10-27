from datetime import datetime
from typing import List
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
from models.wallet import WalletModel
from models.transaction_category import TransactionCategoryModel
from models.transaction_subcategory import TransactionSubcategoryModel
from models.transaction_status import TransactionStatusModel

class Transaction(Base):
    __tablename__ = "Transaction"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    issue_date: Mapped[datetime] = mapped_column(DateTime)

    wallet_id: Mapped[int] = mapped_column(ForeignKey("Wallet.id"))
    wallet: Mapped["Wallet"] = relationship(back_populates="transactions")

    in_out: Mapped[bool] = mapped_column(Boolean)

    amount: Mapped[float] = mapped_column(Float)

    category_id: Mapped[int] = mapped_column(ForeignKey("TransactionCategory.id"))
    category: Mapped["TransactionCategory"] = relationship(back_populates="transactions")

    subcategory_id: Mapped[int] = mapped_column(ForeignKey("TransactionSubcategory.id"))
    subcategory: Mapped["TransactionSubcategory"] = relationship(back_populates="transactions")

    detail: Mapped[str] = mapped_column(String(128))

    status_id: Mapped[int] = mapped_column(ForeignKey("TransactionStatus.id"))
    status: Mapped["TransactionStatus"] = relationship(back_populates="transactions")

    debts: Mapped[List["Debt"]] = relationship(back_populates="transaction")

    created_at: Mapped[datetime] = mapped_column(server_default=func.CURRENT_TIMESTAMP())

    updated_at: Mapped[datetime] = mapped_column(DateTime)

    logical_delete: Mapped[bool] = mapped_column(Boolean)

class TransactionModel(BaseModel):
    id: Optional[int] = None
    issue_date: Optional[datetime] = datetime.now()
    wallet_id: Optional[int] = None
    wallet: Optional[WalletModel] = None
    in_out: Optional[bool] = None
    amount: Optional[float] = None
    category_id: Optional[int] = None
    category: Optional[TransactionCategoryModel] = None
    subcategory_id: Optional[int] = None
    subcategory: Optional[TransactionSubcategoryModel] = None
    detail: Optional[str] = None
    status_id: Optional[int] = None
    status: Optional[TransactionStatusModel] = None