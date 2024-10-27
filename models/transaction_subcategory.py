from datetime import datetime
from typing import List

from fastapi import Query
from pydantic import BaseModel

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import func

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from models.base import Base

class TransactionSubcategory(Base):
    __tablename__ = "TransactionSubcategory"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32))
    transaction_category_id: Mapped[int] = mapped_column(ForeignKey("TransactionCategory.id"))
    transaction_category: Mapped["TransactionCategory"] = relationship(back_populates="subcategories")
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="subcategory")
    created_at: Mapped[datetime] = mapped_column(server_default=func.CURRENT_TIMESTAMP())
    updated_at: Mapped[datetime] = mapped_column(DateTime)
    logical_delete: Mapped[bool] = mapped_column(Boolean)

class TransactionSubcategoryModel(BaseModel):
    id: int
    name: str = Query(default=None, min_length=1)
    transaction_category_id: int