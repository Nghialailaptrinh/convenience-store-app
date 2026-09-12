from dataclasses import dataclass
from uuid import UUID

from application.common.exceptions.not_found import NotFoundError
from application.common.interfaces.application_db_context import ApplicationDbContext
from application.common.interfaces.request import Request
from application.common.interfaces.request_handler import RequestHandler


@dataclass(frozen=True)
class UpdateCartItemQuantityCommand(Request[None]):
    customer_id: UUID
    product_id: UUID
    quantity: int


class UpdateCartItemQuantityCommandHandler(RequestHandler[UpdateCartItemQuantityCommand, None]):
    def __init__(self, context: ApplicationDbContext) -> None:
        self._context = context

    def handle(self, request: UpdateCartItemQuantityCommand) -> None:
        with self._context:
            cart = self._context.carts.get_by_customer_id(request.customer_id)
            if cart is None:
                raise NotFoundError("Cart not found")
            cart.update_quantity(request.product_id, request.quantity)
            self._context.carts.save(cart)
            self._context.save_changes()
