from datetime import datetime
from typing import Optional

from typing import List

from fastapi import Query
from pydantic import BaseModel

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import func

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from models.base import Base


class IdentityType(Base):
    __tablename__ = "IdentityType"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32))
    identities: Mapped[List["Identity"]] = relationship(back_populates="type")
    created_at: Mapped[datetime] = mapped_column(server_default=func.CURRENT_TIMESTAMP())
    updated_at: Mapped[datetime] = mapped_column(DateTime)
    logical_delete: Mapped[bool] = mapped_column(Boolean)

class IdentityTypeModel(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = Query(default=None, min_length=1)
