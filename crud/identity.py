from crud.base import CRUDBase
from models.identity import Identity
from schemas import IdentityCreate, IdentityUpdate

class CRUDIdentity(CRUDBase[Identity, IdentityCreate, IdentityUpdate]):
    pass

identity = CRUDIdentity(Identity)