from dataclasses import dataclass
from uuid import UUID

from application.errors import UseCaseNotImplemented
from domain.entities.product import Product


@dataclass(frozen=True)
class GetProductByIdQuery:
    product_id: UUID


def handle(query: GetProductByIdQuery) -> Product | None:
    raise UseCaseNotImplemented("TODO: implement GetProductById query")
