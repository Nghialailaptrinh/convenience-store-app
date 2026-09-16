from application.orders.commands.create_order.create_order import CreateOrderCommand


class CreateOrderCommandValidator:
    def validate(self, request: CreateOrderCommand) -> None:
        """No client fields. Authentication and ownership are checked inside the handler."""
