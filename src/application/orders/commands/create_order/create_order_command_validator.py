from uuid import UUID

from application.common.exceptions.validation_exception import ValidationException
from application.orders.commands.create_order.create_order import CreateOrderCommand


class CreateOrderCommandValidator:
    def validate(self, request: CreateOrderCommand) -> None:
        errors: dict[str, list[str]] = {}
        if not isinstance(request.customer_id, UUID):
            errors["customer_id"] = ["Must be a UUID"]
        if errors:
            raise ValidationException(errors)
