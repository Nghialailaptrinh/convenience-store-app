from dataclasses import dataclass
from uuid import NAMESPACE_URL, UUID, uuid5

from application.carts.queries.get_cart.cart_dto import CartDto
from application.common.interfaces.application_db_context import ApplicationDbContext
from application.common.interfaces.request import Request
from application.common.interfaces.request_handler import RequestHandler
from domain.entities.cart import Cart


@dataclass(frozen=True)
class GetCartQuery(Request[CartDto]):
    customer_id: UUID


class GetCartQueryHandler(RequestHandler[GetCartQuery, CartDto]):
    def __init__(self, context: ApplicationDbContext) -> None:
        self._context = context

    def handle(self, request: GetCartQuery) -> CartDto:
        with self._context:
            cart = self._context.carts.get_by_customer_id(request.customer_id) or Cart(
                uuid5(NAMESPACE_URL, f"cart:{request.customer_id}"),
                request.customer_id,
            )
            return CartDto.from_domain(cart)
