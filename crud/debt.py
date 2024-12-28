from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.debt import Debt
from models.transaction import Transaction
from models.identity import Identity
from models.category import Category
from models.subcategory import Subcategory
from models.status import Status
from schemas import DebtCreate, DebtUpdate

class CRUDDebt(CRUDBase[Debt, DebtCreate, DebtUpdate]):
    def get_all_debts(self, db: Session):
        return db.query(
            Debt.id,
            Debt.transaction_id,
            Debt.is_income,
            Debt.amount,
            Category.name.label("category"),
            Subcategory.name.label("subcategory"),
            Debt.identity_id,
            Identity.name.label("identity"),
            Debt.detail,
            Debt.status_id,
            Status.name.label("status")
        ).join(
            Transaction, Debt.transaction_id == Transaction.id
        ).join(
            Identity, Debt.identity_id == Identity.id
        ).join(
            Category, Transaction.category_id == Category.id
        ).join(
            Subcategory, Transaction.subcategory_id == Subcategory.id
        ).join(
            Status, Debt.status_id == Status.id
        ).all()

debt = CRUDDebt(Debt)