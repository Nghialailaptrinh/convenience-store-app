from sqlalchemy import create_engine


def create_database_engine(database_url: str = "sqlite:///./shop.db"):
    return create_engine(database_url, future=True)
