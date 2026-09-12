from typing import Protocol
from uuid import UUID

from src.domain.entities.product import Product


class ProductRepository(Protocol):
    def get_all(self) -> list[Product]: ...

    def get_by_id(self, product_id: UUID) -> Product | None: ...
