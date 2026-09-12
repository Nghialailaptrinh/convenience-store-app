from dataclasses import dataclass
from uuid import UUID

from application.common.interfaces.unit_of_work import UnitOfWork
from domain.entities.product import Product


@dataclass(frozen=True)
class GetProductByIdQuery:
    product_id: UUID


def handle(query: GetProductByIdQuery, uow: UnitOfWork) -> Product | None:
    with uow:
        return uow.products.get_by_id(query.product_id)
