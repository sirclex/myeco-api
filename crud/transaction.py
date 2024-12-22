from crud.base import CRUDBase
from models.transaction import Transaction
from schemas import TransactionCreate, TransactionUpdate

class CRUDTransaction(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    pass

transaction = CRUDTransaction(Transaction)