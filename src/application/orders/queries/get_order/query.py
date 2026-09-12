from dataclasses import dataclass
from uuid import UUID

from application.common.interfaces.unit_of_work import UnitOfWork
from domain.entities.order import Order


@dataclass(frozen=True)
class GetOrderQuery:
    order_id: UUID


def handle(query: GetOrderQuery, uow: UnitOfWork) -> Order | None:
    with uow:
        return uow.orders.get_by_id(query.order_id)
