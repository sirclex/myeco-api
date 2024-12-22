from fastapi import APIRouter

from api.v1 import wallets, identity_types, identities, statuses, categories, subcategories, transactions, debts

api_router = APIRouter()
api_router.include_router(wallets.router, prefix="/wallet", tags=["wallets"])
api_router.include_router(identity_types.router, prefix="/identityType", tags=["identity_types"])
api_router.include_router(identities.router, prefix="/identity", tags=["identities"])
api_router.include_router(statuses.router, prefix="/status", tags=["statuses"])
api_router.include_router(categories.router, prefix="/category", tags=["categories"])
api_router.include_router(subcategories.router, prefix="/subcategory", tags=["subcategories"])
api_router.include_router(transactions.router, prefix="/transaction", tags=["transactions"])
api_router.include_router(debts.router, prefix="/debt", tags=["debts"])