from dataclasses import dataclass

from src.domain.entities.product import Product


@dataclass(frozen=True)
class GetProductsQuery:
    include_inactive: bool = False


def handle(query: GetProductsQuery) -> list[Product]:
    raise NotImplementedError("TODO: implement GetProducts query")
