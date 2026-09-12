from dataclasses import dataclass
from uuid import UUID

from application.common.exceptions.not_found import NotFoundError
from application.common.interfaces.unit_of_work import UnitOfWork


@dataclass(frozen=True)
class UpdateCartItemQuantityCommand:
    customer_id: UUID
    product_id: UUID
    quantity: int


def handle(command: UpdateCartItemQuantityCommand, uow: UnitOfWork) -> None:
    with uow:
        cart = uow.carts.get_by_customer_id(command.customer_id)
        if cart is None:
            raise NotFoundError("Cart not found")
        cart.update_quantity(command.product_id, command.quantity)
        uow.carts.save(cart)
        uow.commit()
