from fastapi import APIRouter

from api.v1 import wallets

api_router = APIRouter()
api_router.include_router(wallets.router, prefix="/wallet", tags=["wallets"])