from dataclasses import dataclass
from uuid import UUID

from application.common.exceptions.not_found import NotFoundError
from application.common.interfaces.unit_of_work import UnitOfWork


@dataclass(frozen=True)
class CancelOrderCommand:
    order_id: UUID


def handle(command: CancelOrderCommand, uow: UnitOfWork) -> None:
    with uow:
        order = uow.orders.get_by_id(command.order_id)
        if order is None:
            raise NotFoundError("Order not found")
        order.cancel()
        uow.orders.save(order)
        uow.commit()
