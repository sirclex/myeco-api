from datetime import datetime
from typing import List
from typing import Optional

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
from models.identity_type import IdentityTypeModel

class Identity(Base):
    __tablename__ = "Identity"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32))

    type_id: Mapped[int] = mapped_column(ForeignKey("IdentityType.id"))
    type: Mapped["IdentityType"] = relationship(back_populates="identities")

    debts: Mapped[List["Debt"]] = relationship(back_populates="identity")
    created_at: Mapped[datetime] = mapped_column(server_default=func.CURRENT_TIMESTAMP())
    updated_at: Mapped[datetime] = mapped_column(DateTime)
    logical_delete: Mapped[bool] = mapped_column(Boolean)

class IdentityModel(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = Query(default=None, min_length=1)
    type_id: Optional[int] = None
    type: Optional[IdentityTypeModel] = None