from uuid import UUID

from application.common.exceptions.validation_exception import ValidationException
from application.orders.commands.cancel_order.cancel_order import CancelOrderCommand


class CancelOrderCommandValidator:
    def validate(self, request: CancelOrderCommand) -> None:
        errors: dict[str, list[str]] = {}
        if not isinstance(request.order_id, UUID):
            errors["order_id"] = ["Must be a UUID"]
        if errors:
            raise ValidationException(errors)
