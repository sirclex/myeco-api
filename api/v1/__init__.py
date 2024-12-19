from fastapi import APIRouter

from api.v1 import wallets, identity_types

api_router = APIRouter()
api_router.include_router(wallets.router, prefix="/wallet", tags=["wallets"])
api_router.include_router(identity_types.router, prefix="/identityType", tags=["identity_types"])