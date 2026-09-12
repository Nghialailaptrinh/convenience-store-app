from decimal import Decimal
from uuid import uuid4

import pytest

from domain.entities.cart import Cart
from domain.entities.order import Order
from domain.entities.order_item import OrderItem
from domain.enums.order_status import OrderStatus
from domain.exceptions.business_rule_error import BusinessRuleError
from domain.value_objects.money import Money


@pytest.mark.parametrize("amount", [Decimal(-1), Decimal("NaN"), Decimal("Infinity"), Decimal("1.5"), 1.0])
def test_invalid_money(amount):
    with pytest.raises(BusinessRuleError):
        Money(amount)


def test_cart_quantity_invariant():
    cart = Cart(uuid4(), uuid4())
    product = uuid4()
    cart.add(product, 99)
    with pytest.raises(BusinessRuleError):
        cart.add(product, 1)
    assert cart.items[0].quantity == 99
    with pytest.raises(BusinessRuleError):
        cart.update_quantity(product, 0)
    assert cart.items[0].quantity == 99


def test_order_states_and_snapshot():
    item = OrderItem(uuid4(), 2, Money(Decimal(32000)), "Milk")
    order = Order(id=uuid4(), customer_id=uuid4(), items=[item])
    assert order.total == Money(Decimal(64000))
    order.cancel()
    with pytest.raises(BusinessRuleError):
        order.mark_paid("demo-payment")
    assert order.status == OrderStatus.CANCELLED
    with pytest.raises(BusinessRuleError):
        Order(uuid4(), uuid4())
