from dataclasses import dataclass

from application.common.interfaces.unit_of_work import UnitOfWork
from domain.entities.product import Product


@dataclass(frozen=True)
class GetProductsQuery:
    include_inactive: bool = False


def handle(query: GetProductsQuery, uow: UnitOfWork) -> list[Product]:
    with uow:
        return [p for p in uow.products.get_all() if query.include_inactive or p.is_active]
