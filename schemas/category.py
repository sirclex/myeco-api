from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class CategoryBase(BaseModel):
    name: Optional[str]

class CategoryCreate(CategoryBase):
    name: str
    updated_at: Optional[datetime] = datetime.now()
    logical_delete: bool = False

class CategoryUpdate(CategoryBase):
    id: int
    updated_at: Optional[datetime] = datetime.now()

class CategoryDelete(CategoryBase):
    id: int
    updated_at: Optional[datetime] = datetime.now()
    logical_delete: bool = True

class CategoryResponse(CategoryBase):
    id: Optional[int]
    class Config:
        from_attributes = True