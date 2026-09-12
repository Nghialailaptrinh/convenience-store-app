from uuid import uuid4

import pytest

from domain.entities.cart import Cart
from domain.exceptions.business_rule_error import BusinessRuleError


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
