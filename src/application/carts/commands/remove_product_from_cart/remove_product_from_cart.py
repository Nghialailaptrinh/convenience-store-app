from dataclasses import dataclass
from uuid import UUID

from application.common.interfaces.application_db_context import IApplicationDbContext
from application.common.interfaces.request import Request
from application.common.interfaces.request_handler import RequestHandler


@dataclass(frozen=True)
class RemoveProductFromCartCommand(Request[None]):
    customer_id: UUID
    product_id: UUID


class RemoveProductFromCartCommandHandler(
    RequestHandler[RemoveProductFromCartCommand, None]
):
    def __init__(self, context: IApplicationDbContext) -> None:
        self._context = context

    def handle(self, request: RemoveProductFromCartCommand) -> None:
        with self._context:
            cart = self._context.carts.get_by_customer_id(request.customer_id)
            if cart is not None:
                cart.remove(request.product_id)
                self._context.carts.save(cart)
                self._context.save_changes()
