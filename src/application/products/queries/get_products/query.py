from dataclasses import dataclass

from application.common.exceptions.use_case_not_implemented import UseCaseNotImplemented
from domain.entities.product import Product


@dataclass(frozen=True)
class GetProductsQuery:
    include_inactive: bool = False


def handle(query: GetProductsQuery) -> list[Product]:
    raise UseCaseNotImplemented("TODO: implement GetProducts query")
