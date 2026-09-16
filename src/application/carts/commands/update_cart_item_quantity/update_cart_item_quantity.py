from dataclasses import dataclass
from uuid import UUID

from application.common.exceptions.not_found import NotFoundError
from application.common.interfaces.application_db_context import IApplicationDbContext
from application.common.interfaces.current_user import ICurrentUser
from application.common.interfaces.request import Request
from application.common.interfaces.request_handler import RequestHandler
from application.common.security.require_customer import require_customer


@dataclass(frozen=True)
class UpdateCartItemQuantityCommand(Request[None]):
    product_id: UUID
    quantity: int


class UpdateCartItemQuantityCommandHandler(RequestHandler[UpdateCartItemQuantityCommand, None]):
    def __init__(self, context: IApplicationDbContext, current_user: ICurrentUser | None) -> None:
        self._context = context
        self._current_user = current_user

    def handle(self, request: UpdateCartItemQuantityCommand) -> None:
        with self._context:
            customer_id = require_customer(self._context, self._current_user)
            cart = self._context.carts.get_by_customer_id(customer_id)
            if cart is None:
                raise NotFoundError("Cart not found")
            cart.update_quantity(request.product_id, request.quantity)
            self._context.carts.save(cart)
            self._context.save_changes()
