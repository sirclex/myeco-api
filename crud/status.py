from crud.base import CRUDBase
from models.status import Status
from schemas import StatusCreate, StatusUpdate

class CRUDStatus(CRUDBase[Status, StatusCreate, StatusUpdate]):
    pass

status = CRUDStatus(Status)