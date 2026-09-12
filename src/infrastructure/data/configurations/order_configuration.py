"""Order persistence mapping. JSON items keep the SQLite demo small."""

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.data.configurations.base import Base


class OrderRecord(Base):
    __tablename__ = "orders"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    customer_id: Mapped[str]
    status: Mapped[str]
    items: Mapped[list[dict]] = mapped_column(JSON)
    payment_reference: Mapped[str | None]
