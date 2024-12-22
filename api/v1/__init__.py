from fastapi import APIRouter

from api.v1 import wallets, identity_types, identities, categories

api_router = APIRouter()
api_router.include_router(wallets.router, prefix="/wallet", tags=["wallets"])
api_router.include_router(identity_types.router, prefix="/identityType", tags=["identity_types"])
api_router.include_router(identities.router, prefix="/identity", tags=["identities"])
api_router.include_router(categories.router, prefix="/category", tags=["categories"])