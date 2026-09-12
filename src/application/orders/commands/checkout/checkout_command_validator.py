from uuid import UUID

from application.common.exceptions.validation_exception import ValidationException
from application.orders.commands.checkout.checkout import CheckoutCommand


class CheckoutCommandValidator:
    def validate(self, request: CheckoutCommand) -> None:
        errors: dict[str, list[str]] = {}
        if not isinstance(request.customer_id, UUID):
            errors["customer_id"] = ["Must be a UUID"]
        if errors:
            raise ValidationException(errors)
