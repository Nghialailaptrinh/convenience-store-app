from dataclasses import dataclass
from uuid import UUID

from application.common.exceptions.not_found import NotFoundError
from application.common.interfaces.application_db_context import ApplicationDbContext
from application.common.interfaces.request import Request
from application.common.interfaces.request_handler import RequestHandler


@dataclass(frozen=True)
class CancelOrderCommand(Request[None]):
    order_id: UUID


class CancelOrderCommandHandler(RequestHandler[CancelOrderCommand, None]):
    def __init__(self, context: ApplicationDbContext) -> None:
        self._context = context

    def handle(self, request: CancelOrderCommand) -> None:
        with self._context:
            order = self._context.orders.get_by_id(request.order_id)
            if order is None:
                raise NotFoundError("Order not found")
            order.cancel()
            self._context.orders.save(order)
            self._context.save_changes()
