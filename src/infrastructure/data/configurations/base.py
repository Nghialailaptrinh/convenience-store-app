"""Shared SQLAlchemy metadata; Domain entities remain independent of the ORM."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
