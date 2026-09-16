from dataclasses import dataclass
from uuid import NAMESPACE_URL, uuid5

from application.carts.queries.get_cart.cart_dto import CartDto
from application.common.interfaces.application_db_context import IApplicationDbContext
from application.common.interfaces.current_user import ICurrentUser
from application.common.interfaces.request import Request
from application.common.interfaces.request_handler import RequestHandler
from application.common.security.require_customer import require_customer
from domain.entities.cart import Cart


@dataclass(frozen=True)
class GetCartQuery(Request[CartDto]):
    pass


class GetCartQueryHandler(RequestHandler[GetCartQuery, CartDto]):
    def __init__(self, context: IApplicationDbContext, current_user: ICurrentUser | None) -> None:
        self._context = context
        self._current_user = current_user

    def handle(self, request: GetCartQuery) -> CartDto:
        with self._context:
            customer_id = require_customer(self._context, self._current_user)
            cart = self._context.carts.get_by_customer_id(customer_id) or Cart(
                uuid5(NAMESPACE_URL, f"cart:{customer_id}"),
                customer_id,
            )
            return CartDto.from_domain(cart)
