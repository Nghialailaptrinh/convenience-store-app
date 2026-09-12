from dataclasses import dataclass
from uuid import NAMESPACE_URL, UUID, uuid5

from application.common.exceptions.not_found import NotFoundError
from application.common.interfaces.unit_of_work import UnitOfWork
from domain.entities.cart import Cart
from domain.exceptions.business_rule_error import BusinessRuleError


@dataclass(frozen=True)
class AddProductToCartCommand:
    customer_id: UUID
    product_id: UUID
    quantity: int


def handle(command: AddProductToCartCommand, uow: UnitOfWork) -> None:
    with uow:
        product = uow.products.get_by_id(command.product_id)
        if product is None:
            raise NotFoundError("Product not found")
        if not product.is_active:
            raise BusinessRuleError("Product is unavailable")
        cart = uow.carts.get_by_customer_id(command.customer_id) or Cart(
            uuid5(NAMESPACE_URL, f"cart:{command.customer_id}"), command.customer_id,
        )
        cart.add(command.product_id, command.quantity)
        uow.carts.save(cart)
        uow.commit()
