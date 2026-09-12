from dataclasses import dataclass
from uuid import NAMESPACE_URL, UUID, uuid5

from application.common.interfaces.unit_of_work import UnitOfWork
from domain.entities.cart import Cart


@dataclass(frozen=True)
class GetCartQuery:
    customer_id: UUID


def handle(query: GetCartQuery, uow: UnitOfWork) -> Cart:
    with uow:
        return uow.carts.get_by_customer_id(query.customer_id) or Cart(
            uuid5(NAMESPACE_URL, f"cart:{query.customer_id}"), query.customer_id,
        )
