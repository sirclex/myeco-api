import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    API_KEY: str = os.getenv("API_KEY")
    API_KEY_NAME: str = os.getenv("API_KEY_NAME")

    CORS_ORIGIN: str = os.getenv("CORS_ORIGIN")

    class Config:
        env_file =".env"

settings = Settings()