from uuid import UUID

from application.carts.commands.update_cart_item_quantity.update_cart_item_quantity import (
    UpdateCartItemQuantityCommand,
)
from application.common.exceptions.validation_exception import ValidationException


class UpdateCartItemQuantityCommandValidator:
    def validate(self, request: UpdateCartItemQuantityCommand) -> None:
        errors: dict[str, list[str]] = {}
        if not isinstance(request.product_id, UUID):
            errors["product_id"] = ["Must be a UUID"]
        if type(request.quantity) is not int or not 1 <= request.quantity <= 99:
            errors["quantity"] = ["Must be an integer from 1 to 99"]
        if errors:
            raise ValidationException(errors)
