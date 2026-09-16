from dataclasses import dataclass
from uuid import UUID

from application.common.exceptions.not_found import NotFoundError
from application.common.interfaces.application_db_context import IApplicationDbContext
from application.common.interfaces.current_user import ICurrentUser
from application.common.interfaces.request import Request
from application.common.interfaces.request_handler import RequestHandler
from application.common.security.require_customer import require_customer


@dataclass(frozen=True)
class CancelOrderCommand(Request[None]):
    order_id: UUID


class CancelOrderCommandHandler(RequestHandler[CancelOrderCommand, None]):
    def __init__(self, context: IApplicationDbContext, current_user: ICurrentUser | None) -> None:
        self._context = context
        self._current_user = current_user

    def handle(self, request: CancelOrderCommand) -> None:
        with self._context:
            customer_id = require_customer(self._context, self._current_user)
            order = self._context.orders.get_by_id(request.order_id)
            if order is None or order.customer_id != customer_id:
                raise NotFoundError("Order not found")
            order.cancel()
            self._context.orders.save(order)
            self._context.save_changes()
