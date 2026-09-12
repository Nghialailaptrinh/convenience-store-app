from typing import Protocol
from uuid import UUID

from domain.entities.product import Product


class IProductRepository(Protocol):
    def get_all(self) -> list[Product]: ...

    def get_by_id(self, product_id: UUID) -> Product | None: ...
