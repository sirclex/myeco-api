from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    def __init__(self, engine):
        self.engine = engine

    def create_all(self):
        self.metadata.create_all(self.engine)