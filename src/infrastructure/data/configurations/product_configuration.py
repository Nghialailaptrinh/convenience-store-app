"""Product persistence mapping corresponding to ProductConfiguration in the template."""

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.data.configurations.base import Base


class ProductRecord(Base):
    __tablename__ = "products"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    amount: Mapped[str]
    currency: Mapped[str]
    category_id: Mapped[str]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
