from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware

from api.v1 import api_router
from core import settings, get_api_key

origins = {settings.CORS_ORIGIN}

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"]
)
    
app.include_router(api_router, prefix="/myeco", dependencies=[Security(get_api_key)])