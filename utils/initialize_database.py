import os

from dotenv import load_dotenv
from models.base import Base
from models.wallet import Wallet
from models.identity_type import IdentityType
from models.identity import Identity
from models.transaction_category import TransactionCategory
from models.transaction_subcategory import TransactionSubcategory
from models.transaction_status import TransactionStatus
from models.transaction import Transaction
from models.debt import Debt

from sqlalchemy import create_engine

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"), echo=True, pool_pre_ping=True)

def initialize_database():
    base = Base(engine=engine)
    base.create_all()