from uuid import UUID

from sqlalchemy.orm import Session

from application.interfaces.product_repository import ProductRepository
from domain.entities.product import Product


class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> list[Product]:
        raise NotImplementedError("TODO: map SQLAlchemy models to domain products")

    def get_by_id(self, product_id: UUID) -> Product | None:
        raise NotImplementedError("TODO: load product by id")
