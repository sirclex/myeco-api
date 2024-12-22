from sqlalchemy import Column, Integer, String, DateTime, Boolean, func

from database.base_class import Base


class Subcategory(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    category_id = Column(Integer)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime)
    logical_delete = Column(Boolean)