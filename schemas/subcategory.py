from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class SubcategoryBase(BaseModel):
    name: Optional[str]
    category_id: Optional[int]

class SubcategoryCreate(SubcategoryBase):
    name: str
    category_id: int
    updated_at: Optional[datetime] = datetime.now()
    logical_delete: bool = False

class SubcategoryUpdate(SubcategoryBase):
    id: int
    updated_at: Optional[datetime] = datetime.now()

class SubcategoryDelete(SubcategoryBase):
    id: int
    updated_at: Optional[datetime] = datetime.now()
    logical_delete: bool = True

class SubcategoryResponse(SubcategoryBase):
    id: Optional[int]
    class Config:
        from_attributes = True