from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.data.configurations.base import Base


class CustomerRecord(Base):
    __tablename__ = "customers"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), nullable=True, unique=True)
