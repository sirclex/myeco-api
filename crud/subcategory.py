from crud.base import CRUDBase
from models.subcategory import Subcategory
from schemas import SubcategoryCreate, SubcategoryUpdate

class CRUDSubcategory(CRUDBase[Subcategory, SubcategoryCreate, SubcategoryUpdate]):
    def get_by_category_id(self, db, category_id: int):
        return db.query(Subcategory).filter(Subcategory.category_id == category_id).all()

subcategory = CRUDSubcategory(Subcategory)