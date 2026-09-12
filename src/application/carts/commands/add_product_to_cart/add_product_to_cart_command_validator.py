from uuid import UUID

from application.carts.commands.add_product_to_cart.add_product_to_cart import (
    AddProductToCartCommand,
)
from application.common.exceptions.validation_exception import ValidationException


class AddProductToCartCommandValidator:
    def validate(self, request: AddProductToCartCommand) -> None:
        errors: dict[str, list[str]] = {}
        if not isinstance(request.customer_id, UUID):
            errors["customer_id"] = ["Must be a UUID"]
        if not isinstance(request.product_id, UUID):
            errors["product_id"] = ["Must be a UUID"]
        if type(request.quantity) is not int or not 1 <= request.quantity <= 99:
            errors["quantity"] = ["Must be an integer from 1 to 99"]
        if errors:
            raise ValidationException(errors)
