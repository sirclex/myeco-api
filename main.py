from datetime import datetime
from typing import Union, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

origins = {
    "http://localhost:3000"
}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)

from models.wallet import WalletModel
from models.identity import IdentityModel
from models.transaction import TransactionModel
from models.debt import DebtModel

from utils import wallet_logic
from utils import identity_logic
from utils import transaction_logic
from utils import debt_logic
from utils import category_logic
from utils import subcategory_logic

from utils.initialize_database import initialize_database, engine
# from sqlalchemy.orm import Session

# from sqlalchemy import select

initialize_database()

# Wallet
@app.post("/wallet/create")
async def create_wallet(wallet: WalletModel):
    return wallet_logic.create_wallet(wallet=wallet, engine=engine)

@app.get("/wallets")
async def get_wallets():
    return wallet_logic.get_all_wallets(engine)

@app.get("/wallet")
async def get_wallet(id: int):
    return wallet_logic.get_wallet(id, engine)

@app.post("/wallet/delete")
async def delete_wallet(id: int):
    return wallet_logic.delete_wallet(id, engine)

@app.post("/wallet/revive")
async def delete_wallet(id: int):
    return wallet_logic.revive_wallet(id, engine)

@app.post("/wallet/update")
async def update_wallet(wallet: WalletModel):
    return wallet_logic.update_wallet(wallet, engine)

#Identity
@app.post("/identity/create")
async def create_identity(identity: IdentityModel):
    return identity_logic.create_identity(identity, engine)

@app.get("/identities")
async def get_identities():
    return identity_logic.get_all_identities(engine)

@app.get("/identity")
async def get_identity(id: int):
    return identity_logic.get_identity(id, engine)

@app.post("/identity/delete")
async def delete_identity(id: int):
    return identity_logic.delete_identity(id, engine)

@app.post("/identity/revive")
async def revive_identity(id: int):
    return identity_logic.revive_identity(id, engine)

@app.post("/identity/update")
async def update_identity(identity: IdentityModel):
    return identity_logic.update_identity(identity, engine)

# TODO Transaction Category
@app.get("/categories")
async def get_categories():
    return category_logic.get_all_categories(engine)

# TODO Transaction Subcategory
# @app.get("/allsubcategories")
# async def get_subcategories():
#     return subcategory_logic.get_all_subcategories(engine)

@app.get("/subcategories")
async def get_subcategories(category_id: int):
    return subcategory_logic.get_subcategories(engine, category_id)

# Transaction
@app.post("/transaction/create")
async def create_transaction(transaction: TransactionModel, debts: List[DebtModel]):
    transaction_id = transaction_logic.create_transaction(transaction, engine)
    if len(debts) > 0:
        for debt in debts:
            debt.transaction_id = transaction_id
        debt_logic.create_multiple_debt(debts=debts, engine=engine)

@app.get("/transactions")
async def get_transactions():
    return transaction_logic.get_all_transactions(engine)

@app.get("/transaction")
async def get_transaction(id: int):
    return transaction_logic.get_transaction(id, engine)

@app.post("/transaction/delete")
async def delete_transaction(id: int):
    return transaction_logic.delete_transaction(id, engine)

@app.post("/transaction/revive")
async def revive_transaction(id: int):
    return transaction_logic.revive_transaction(id, engine)

@app.post("/transaction/update")
async def update_transaction(transaction: TransactionModel):
    return transaction_logic.update_transaction(transaction, engine)

# Debt
@app.post("/debt/create")
async def create_debt(debt: DebtModel):
    return debt_logic.create_debt(debt, engine)

@app.get("/debts")
async def get_debts():
    return debt_logic.get_all_debts(engine)

@app.get("/debt")
async def get_debt(id: int):
    return debt_logic.get_debt(id, engine)

@app.post("/debt/delete")
async def delete_debt(id: int):
    return debt_logic.delete_debt(id, engine)

@app.post("/debt/revive")
async def revive_debt(id: int):
    return debt_logic.revive_debt(id, engine)

@app.post("/debt/update")
async def update_debt(debt: DebtModel):
    return debt_logic.update_debt(debt, engine)