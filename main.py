import os

from datetime import datetime
from typing import Union, List

from dotenv import load_dotenv

from fastapi import FastAPI, Security, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader

load_dotenv()

origins = {os.getenv("CORS_ORIGIN")}

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"]
)

api_key_header = APIKeyHeader(name=os.getenv("API_KEY_NAME"), auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == f"Bearer {os.getenv("API_KEY")}":
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

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
async def create_wallet(wallet: WalletModel, api_key: str = Security(get_api_key)):
    return wallet_logic.create_wallet(wallet=wallet, engine=engine)


@app.get("/wallets")
async def get_wallets(api_key: str = Security(get_api_key)):
    return wallet_logic.get_all_wallets(engine)


@app.get("/wallet")
async def get_wallet(id: int, api_key: str = Security(get_api_key)):
    return wallet_logic.get_wallet(id, engine)


@app.post("/wallet/delete")
async def delete_wallet(id: int, api_key: str = Security(get_api_key)):
    return wallet_logic.delete_wallet(id, engine)


@app.post("/wallet/revive")
async def delete_wallet(id: int, api_key: str = Security(get_api_key)):
    return wallet_logic.revive_wallet(id, engine)


@app.post("/wallet/update")
async def update_wallet(wallet: WalletModel, api_key: str = Security(get_api_key)):
    return wallet_logic.update_wallet(wallet, engine)


# Identity
@app.post("/identity/create")
async def create_identity(identity: IdentityModel, api_key: str = Security(get_api_key)):
    return identity_logic.create_identity(identity, engine)


@app.get("/identities")
async def get_identities(api_key: str = Security(get_api_key)):
    return identity_logic.get_all_identities(engine)


@app.get("/identity")
async def get_identity(id: int, api_key: str = Security(get_api_key)):
    return identity_logic.get_identity(id, engine)


@app.post("/identity/delete")
async def delete_identity(id: int, api_key: str = Security(get_api_key)):
    return identity_logic.delete_identity(id, engine)


@app.post("/identity/revive")
async def revive_identity(id: int, api_key: str = Security(get_api_key)):
    return identity_logic.revive_identity(id, engine)


@app.post("/identity/update")
async def update_identity(identity: IdentityModel, api_key: str = Security(get_api_key)):
    return identity_logic.update_identity(identity, engine)


# TODO Transaction Category
@app.get("/categories")
async def get_categories(api_key: str = Security(get_api_key)):
    return category_logic.get_all_categories(engine)


# TODO Transaction Subcategory
# @app.get("/allsubcategories")
# async def get_subcategories():
#     return subcategory_logic.get_all_subcategories(engine)


@app.get("/subcategories")
async def get_subcategories(category_id: int, api_key: str = Security(get_api_key)):
    return subcategory_logic.get_subcategories(engine, category_id)


# Transaction
@app.post("/transaction/create")
async def create_transaction(transaction: TransactionModel, debts: List[DebtModel], api_key: str = Security(get_api_key)):
    transaction_id = transaction_logic.create_transaction(transaction, engine)
    if len(debts) > 0:
        for debt in debts:
            debt.transaction_id = transaction_id
        debt_logic.create_multiple_debt(debts=debts, engine=engine)


@app.get("/transactions")
async def get_transactions(api_key: str = Security(get_api_key)):
    return transaction_logic.get_all_transactions(engine)


@app.get("/transaction")
async def get_transaction(id: int, api_key: str = Security(get_api_key)):
    return transaction_logic.get_transaction(id, engine)


@app.post("/transaction/delete")
async def delete_transaction(id: int, api_key: str = Security(get_api_key)):
    return transaction_logic.delete_transaction(id, engine)


@app.post("/transaction/revive")
async def revive_transaction(id: int, api_key: str = Security(get_api_key)):
    return transaction_logic.revive_transaction(id, engine)


@app.post("/transaction/update")
async def update_transaction(transaction: TransactionModel, api_key: str = Security(get_api_key)):
    return transaction_logic.update_transaction(transaction, engine)


# Debt
@app.post("/debt/create")
async def create_debt(debt: DebtModel, api_key: str = Security(get_api_key)):
    return debt_logic.create_debt(debt, engine)


@app.get("/debts")
async def get_debts(api_key: str = Security(get_api_key)):
    result = debt_logic.get_all_debts(engine)
    response = []
    for row in result:
        response.append({
            "id": row.id,
            "transaction_id": row.transaction_id,
            "issue_date": row.issue_date,
            "in_out": row.in_out,
            "wallet": row.wallet,
            "amount": row.amount,
            "detail": row.detail,
            "identity" : row.identity,
            "status_id": row.status_id
        })
    return response

@app.get("/pendingDebt")
async def get_sum_debts_by_identity(api_key: str = Security(get_api_key)):
    result = debt_logic.get_sum_debt_by_identity(engine)
    response = []
    for row in result:
        response.append({
            "name": row.name,
            "amount": row.amount,
            "isIncome": row.in_out
        })
    return response

@app.post("/setDoneDebt")
async def set_done_debt(debt_ids: List[int], api_key: str = Security(get_api_key)):
    result = debt_logic.update_debt_status(debt_ids=debt_ids, status_id=2, engine=engine)
    transaction_ids = []
    for record in result:
        transaction_ids.append(*record)

    statuses = debt_logic.check_transaction_status(transaction_ids, engine)
    if (len(transaction_ids) != len(statuses)):
        return None

    transaction_ids_done = []
    transaction_ids_pending = []
    for i in range(len(transaction_ids)):
        if (statuses[i]):
            transaction_ids_pending.append(transaction_ids[i])
        else:
            transaction_ids_done.append(transaction_ids[i])

    if (len(transaction_ids_done) > 0):
        transaction_logic.update_transaction_status(transaction_ids=transaction_ids_done, status_id=2, engine=engine)
    
    if (len(transaction_ids_pending) > 0):
        transaction_logic.update_transaction_status(transaction_ids=transaction_ids_pending, status_id=1, engine=engine)

    return len(transaction_ids)


@app.post("/debt/delete")
async def delete_debt(id: int, api_key: str = Security(get_api_key)):
    return debt_logic.delete_debt(id, engine)


@app.post("/debt/revive")
async def revive_debt(id: int, api_key: str = Security(get_api_key)):
    return debt_logic.revive_debt(id, engine)


@app.post("/debt/update")
async def update_debt(debt: DebtModel, api_key: str = Security(get_api_key)):
    return debt_logic.update_debt(debt, engine)
