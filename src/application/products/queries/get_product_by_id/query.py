from dataclasses import dataclass
from uuid import UUID

from application.common.exceptions.use_case_not_implemented import UseCaseNotImplemented
from domain.entities.product import Product


@dataclass(frozen=True)
class GetProductByIdQuery:
    product_id: UUID


def handle(query: GetProductByIdQuery) -> Product | None:
    raise UseCaseNotImplemented("TODO: implement GetProductById query")
