from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core import settings
from models import wallet

engine = create_engine(settings.DATABASE_URL, echo=True, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

wallet.Base.metadata.create_all(bind=engine)