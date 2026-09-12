from uuid import UUID

from src.domain.entities.product import Product


class SqlAlchemyProductRepository:
    def get_all(self) -> list[Product]:
        raise NotImplementedError("TODO: map SQLAlchemy models to domain products")

    def get_by_id(self, product_id: UUID) -> Product | None:
        raise NotImplementedError("TODO: load product by id")
