from dataclasses import dataclass
from uuid import NAMESPACE_URL, UUID, uuid5

from application.common.exceptions.not_found import NotFoundError
from application.common.interfaces.application_db_context import IApplicationDbContext
from application.common.interfaces.current_user import ICurrentUser
from application.common.interfaces.request import Request
from application.common.interfaces.request_handler import RequestHandler
from application.common.security.require_customer import require_customer
from domain.entities.cart import Cart
from domain.exceptions.business_rule_error import BusinessRuleError


@dataclass(frozen=True)
class AddProductToCartCommand(Request[None]):
    product_id: UUID
    quantity: int


class AddProductToCartCommandHandler(RequestHandler[AddProductToCartCommand, None]):
    def __init__(self, context: IApplicationDbContext, current_user: ICurrentUser | None) -> None:
        self._context = context
        self._current_user = current_user

    def handle(self, request: AddProductToCartCommand) -> None:
        with self._context:
            customer_id = require_customer(self._context, self._current_user)
            product = self._context.products.get_by_id(request.product_id)
            if product is None:
                raise NotFoundError("Product not found")
            if not product.is_active:
                raise BusinessRuleError("Product is unavailable")
            cart = self._context.carts.get_by_customer_id(customer_id) or Cart(
                uuid5(NAMESPACE_URL, f"cart:{customer_id}"),
                customer_id,
            )
            cart.add(request.product_id, request.quantity)
            self._context.carts.save(cart)
            self._context.save_changes()
