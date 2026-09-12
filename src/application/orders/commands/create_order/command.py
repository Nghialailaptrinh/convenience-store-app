from dataclasses import dataclass
from uuid import UUID, uuid4

from application.common.interfaces.unit_of_work import UnitOfWork
from domain.entities.order import Order
from domain.entities.order_item import OrderItem
from domain.exceptions.business_rule_error import BusinessRuleError


@dataclass(frozen=True)
class CreateOrderCommand:
    customer_id: UUID


def build_order(customer_id: UUID, uow: UnitOfWork) -> Order:
    """Build a price snapshot and consume the cart inside the caller's transaction."""
    cart = uow.carts.get_by_customer_id(customer_id)
    if cart is None or not cart.items:
        raise BusinessRuleError("Cart is empty")
    items = []
    for item in cart.items:
        product = uow.products.get_by_id(item.product_id)
        if product is None or not product.is_active:
            raise BusinessRuleError("A product in the cart is unavailable")
        items.append(OrderItem(product.id, item.quantity, product.price, product.name))
    order = Order(id=uuid4(), customer_id=customer_id, items=items)
    cart.clear()
    uow.carts.save(cart)
    return order


def handle(command: CreateOrderCommand, uow: UnitOfWork) -> UUID:
    with uow:
        order = build_order(command.customer_id, uow)
        uow.orders.save(order)
        uow.commit()
        return order.id
