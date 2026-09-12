"""Persistence records. JSON items keep this SQLite demo deliberately small."""
from sqlalchemy import JSON, Boolean, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ProductRecord(Base):
    __tablename__ = "products"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    amount: Mapped[str]
    currency: Mapped[str]
    category_id: Mapped[str]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class CartRecord(Base):
    __tablename__ = "carts"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    customer_id: Mapped[str] = mapped_column(String(36), unique=True)
    items: Mapped[list[dict]] = mapped_column(JSON)


class OrderRecord(Base):
    __tablename__ = "orders"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    customer_id: Mapped[str]
    status: Mapped[str]
    items: Mapped[list[dict]] = mapped_column(JSON)
    payment_reference: Mapped[str | None]
