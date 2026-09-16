from uuid import UUID

from application.carts.commands.remove_product_from_cart.remove_product_from_cart import (
    RemoveProductFromCartCommand,
)
from application.common.exceptions.validation_exception import ValidationException


class RemoveProductFromCartCommandValidator:
    def validate(self, request: RemoveProductFromCartCommand) -> None:
        errors: dict[str, list[str]] = {}
        if not isinstance(request.product_id, UUID):
            errors["product_id"] = ["Must be a UUID"]
        if errors:
            raise ValidationException(errors)
