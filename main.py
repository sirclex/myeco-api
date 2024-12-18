from fastapi import FastAPI, Security, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader

from api.v1 import api_router
from core import settings

origins = {settings.CORS_ORIGIN}

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"]
)

api_key_header = APIKeyHeader(name=settings.API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == f"Bearer {settings.API_KEY}":
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    
app.include_router(api_router, prefix="/myeco")