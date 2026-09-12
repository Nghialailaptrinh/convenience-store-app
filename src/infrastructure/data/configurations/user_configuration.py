from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.data.configurations.base import Base


class UserRecord(Base):
    """Persistence mapping for local identity accounts."""

    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
