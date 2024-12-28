from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.transaction import Transaction
from models.wallet import Wallet
from models.category import Category
from models.status import Status
from models.subcategory import Subcategory
from schemas import TransactionCreate, TransactionUpdate

class CRUDTransaction(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    def get_transaction_info(self, db: Session):
        return db.query(
            Transaction.id,
            Transaction.wallet_id,
            Wallet.name.label("wallet"),
            Transaction.is_income,
            Transaction.amount,
            Transaction.category_id,
            Category.name.label("category"),
            Transaction.subcategory_id,
            Subcategory.name.label("subcategory"),
            Transaction.detail,
            Transaction.status_id,
            Status.name.label("status")
        ).join(
            Wallet, Transaction.wallet_id == Wallet.id
        ).join(
            Category, Transaction.category_id == Category.id
        ).join(
            Subcategory, Transaction.subcategory_id == Subcategory.id
        ).join(
            Status, Transaction.status_id == Status.id
        ).all()

transaction = CRUDTransaction(Transaction)