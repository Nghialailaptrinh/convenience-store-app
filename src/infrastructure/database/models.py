"""Define ORM tables here, separately from Domain dataclasses.

TODO: tables and explicit domain mappings when persistence is implemented.
Schema creation/migrations must be explicit, never run during module import.
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
