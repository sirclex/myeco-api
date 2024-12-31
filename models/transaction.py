from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, func

from database.base_class import Base


class Transaction(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    issue_at = Column(DateTime)
    wallet_id = Column(Integer)
    is_income = Column(Boolean)
    amount = Column(Float)
    category_id = Column(Integer)
    subcategory_id = Column(Integer)
    detail = Column(String(128))
    status_id = Column(Integer)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime)
    logical_delete = Column(Boolean)