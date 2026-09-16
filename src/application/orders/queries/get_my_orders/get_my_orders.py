from dataclasses import dataclass

from application.common.interfaces.application_db_context import IApplicationDbContext
from application.common.interfaces.current_user import ICurrentUser
from application.common.interfaces.request import Request
from application.common.interfaces.request_handler import RequestHandler
from application.common.security.require_customer import require_customer
from application.orders.queries.get_order.order_dto import OrderDto


@dataclass(frozen=True)
class GetMyOrdersQuery(Request[list[OrderDto]]):
    pass


class GetMyOrdersQueryHandler(RequestHandler[GetMyOrdersQuery, list[OrderDto]]):
    def __init__(self, context: IApplicationDbContext, current_user: ICurrentUser | None) -> None:
        self._context = context
        self._current_user = current_user

    def handle(self, request: GetMyOrdersQuery) -> list[OrderDto]:
        with self._context:
            customer_id = require_customer(self._context, self._current_user)
            return [
                OrderDto.from_domain(order)
                for order in self._context.orders.get_by_customer_id(customer_id)
            ]
