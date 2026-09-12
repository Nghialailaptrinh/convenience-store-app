from dataclasses import dataclass
from uuid import UUID

from application.common.interfaces.unit_of_work import UnitOfWork


@dataclass(frozen=True)
class RemoveProductFromCartCommand:
    customer_id: UUID
    product_id: UUID


def handle(command: RemoveProductFromCartCommand, uow: UnitOfWork) -> None:
    with uow:
        cart = uow.carts.get_by_customer_id(command.customer_id)
        if cart is not None:
            cart.remove(command.product_id)
            uow.carts.save(cart)
            uow.commit()
