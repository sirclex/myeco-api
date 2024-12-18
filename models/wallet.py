from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, func

from database.base_class import Base


class Wallet(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    provider = Column(String(32), nullable=False)
    number = Column(String(128))
    balance = Column(Float)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime)
    logical_delete = Column(Boolean)