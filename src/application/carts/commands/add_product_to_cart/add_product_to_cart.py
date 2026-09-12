from dataclasses import dataclass
from uuid import NAMESPACE_URL, UUID, uuid5

from application.common.exceptions.not_found import NotFoundError
from application.common.interfaces.application_db_context import ApplicationDbContext
from application.common.interfaces.request import Request
from application.common.interfaces.request_handler import RequestHandler
from domain.entities.cart import Cart
from domain.exceptions.business_rule_error import BusinessRuleError


@dataclass(frozen=True)
class AddProductToCartCommand(Request[None]):
    customer_id: UUID
    product_id: UUID
    quantity: int


class AddProductToCartCommandHandler(RequestHandler[AddProductToCartCommand, None]):
    def __init__(self, context: ApplicationDbContext) -> None:
        self._context = context

    def handle(self, request: AddProductToCartCommand) -> None:
        with self._context:
            product = self._context.products.get_by_id(request.product_id)
            if product is None:
                raise NotFoundError("Product not found")
            if not product.is_active:
                raise BusinessRuleError("Product is unavailable")
            cart = self._context.carts.get_by_customer_id(request.customer_id) or Cart(
                uuid5(NAMESPACE_URL, f"cart:{request.customer_id}"),
                request.customer_id,
            )
            cart.add(request.product_id, request.quantity)
            self._context.carts.save(cart)
            self._context.save_changes()
