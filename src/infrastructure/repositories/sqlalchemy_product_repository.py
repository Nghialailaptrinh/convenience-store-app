from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from application.common.interfaces.product_repository import IProductRepository
from domain.entities.product import Product
from domain.value_objects.money import Money
from infrastructure.data.configurations.product_configuration import ProductRecord


def to_product(row: ProductRecord) -> Product:
    return Product(
        UUID(row.id),
        row.name,
        row.description,
        Money(Decimal(row.amount), row.currency),
        UUID(row.category_id),
        row.is_active,
    )


class SqlAlchemyProductRepository(IProductRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> list[Product]:
        return [
            to_product(row)
            for row in self.session.scalars(
                select(ProductRecord).order_by(ProductRecord.id)
            )
        ]

    def get_by_id(self, product_id: UUID) -> Product | None:
        row = self.session.get(ProductRecord, str(product_id))
        return to_product(row) if row is not None else None
