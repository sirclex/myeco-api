from crud.base import CRUDBase
from models.identity_type import IdentityType
from schemas import IdentityTypeCreate, IdentityTypeUpdate

class CRUDIdentityType(CRUDBase[IdentityType, IdentityTypeCreate, IdentityTypeUpdate]):
    pass

identity_type = CRUDIdentityType(IdentityType)