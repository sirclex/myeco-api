from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, func

from database.base_class import Base


class Debt(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(Integer)
    is_income = Column(Boolean)
    amount = Column(Float)
    identity_id = Column(Integer)
    detail = Column(String(128))
    status_id = Column(Integer)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime)
    logical_delete = Column(Boolean)