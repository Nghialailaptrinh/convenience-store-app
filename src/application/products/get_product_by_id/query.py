from dataclasses import dataclass
from uuid import UUID

from src.domain.entities.product import Product


@dataclass(frozen=True)
class GetProductByIdQuery:
    product_id: UUID


def handle(query: GetProductByIdQuery) -> Product | None:
    raise NotImplementedError("TODO: implement GetProductById query")
