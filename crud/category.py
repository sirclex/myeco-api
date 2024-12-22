from crud.base import CRUDBase
from models.category import Category
from schemas import CategoryCreate, CategoryUpdate

class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    pass

category = CRUDCategory(Category)