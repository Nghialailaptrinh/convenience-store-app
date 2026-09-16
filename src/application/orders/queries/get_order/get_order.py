from dataclasses import dataclass
from uuid import UUID

from application.common.interfaces.application_db_context import IApplicationDbContext
from application.common.interfaces.current_user import ICurrentUser
from application.common.interfaces.request import Request
from application.common.interfaces.request_handler import RequestHandler
from application.common.security.require_customer import require_customer
from application.orders.queries.get_order.order_dto import OrderDto


@dataclass(frozen=True)
class GetOrderQuery(Request[OrderDto | None]):
    order_id: UUID


class GetOrderQueryHandler(RequestHandler[GetOrderQuery, OrderDto | None]):
    def __init__(self, context: IApplicationDbContext, current_user: ICurrentUser | None) -> None:
        self._context = context
        self._current_user = current_user

    def handle(self, request: GetOrderQuery) -> OrderDto | None:
        with self._context:
            customer_id = require_customer(self._context, self._current_user)
            order = self._context.orders.get_by_id(request.order_id)
            return (
                OrderDto.from_domain(order) if order and order.customer_id == customer_id else None
            )
