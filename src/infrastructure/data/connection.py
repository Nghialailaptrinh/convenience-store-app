import os

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


def create_database_engine(database_url: str | None = None) -> Engine:
    return create_engine(database_url or os.getenv("DATABASE_URL", "sqlite:///./shop.db"))


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, expire_on_commit=False)
