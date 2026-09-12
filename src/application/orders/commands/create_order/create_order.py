from dataclasses import dataclass
from uuid import UUID

from application.common.interfaces.application_db_context import IApplicationDbContext
from application.common.interfaces.request import Request
from application.common.interfaces.request_handler import RequestHandler
from application.orders.common.build_order import build_order


@dataclass(frozen=True)
class CreateOrderCommand(Request[UUID]):
    customer_id: UUID


class CreateOrderCommandHandler(RequestHandler[CreateOrderCommand, UUID]):
    def __init__(self, context: IApplicationDbContext) -> None:
        self._context = context

    def handle(self, request: CreateOrderCommand) -> UUID:
        with self._context:
            order = build_order(request.customer_id, self._context)
            self._context.orders.save(order)
            self._context.save_changes()
            return order.id
