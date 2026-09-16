from dataclasses import dataclass
from uuid import UUID

from application.common.interfaces.application_db_context import IApplicationDbContext
from application.common.interfaces.current_user import ICurrentUser
from application.common.interfaces.request import Request
from application.common.interfaces.request_handler import RequestHandler
from application.common.security.require_customer import require_customer


@dataclass(frozen=True)
class RemoveProductFromCartCommand(Request[None]):
    product_id: UUID


class RemoveProductFromCartCommandHandler(RequestHandler[RemoveProductFromCartCommand, None]):
    def __init__(self, context: IApplicationDbContext, current_user: ICurrentUser | None) -> None:
        self._context = context
        self._current_user = current_user

    def handle(self, request: RemoveProductFromCartCommand) -> None:
        with self._context:
            customer_id = require_customer(self._context, self._current_user)
            cart = self._context.carts.get_by_customer_id(customer_id)
            if cart is not None:
                cart.remove(request.product_id)
                self._context.carts.save(cart)
            self._context.save_changes()
