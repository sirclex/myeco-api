from crud.base import CRUDBase
from models.debt import Debt
from schemas import DebtCreate, DebtUpdate

class CRUDDebt(CRUDBase[Debt, DebtCreate, DebtUpdate]):
    pass

debt = CRUDDebt(Debt)