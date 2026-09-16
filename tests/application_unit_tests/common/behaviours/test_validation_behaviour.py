from uuid import uuid4

import pytest

from application.carts.commands.add_product_to_cart.add_product_to_cart import (
    AddProductToCartCommand,
)
from application.common.exceptions.validation_exception import ValidationException
from application.dependency_injection import create_sender


class UnusedPayment:
    def charge(self, customer_id, amount):
        raise AssertionError("Invalid requests must not invoke payment")


def unexpected_context():
    raise AssertionError("Validate before constructing persistence dependencies")


@pytest.mark.parametrize("quantity", [0, 100, True, 1.5])
def test_validation_precedes_handler_construction(quantity):
    sender = create_sender(unexpected_context, UnusedPayment())
    with pytest.raises(ValidationException) as error:
        sender.send(AddProductToCartCommand(uuid4(), quantity))
    assert "quantity" in error.value.errors
