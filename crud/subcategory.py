from crud.base import CRUDBase
from models.subcategory import Subcategory
from schemas import SubcategoryCreate, SubcategoryUpdate

class CRUDSubcategory(CRUDBase[Subcategory, SubcategoryCreate, SubcategoryUpdate]):
    pass

subcategory = CRUDSubcategory(Subcategory)