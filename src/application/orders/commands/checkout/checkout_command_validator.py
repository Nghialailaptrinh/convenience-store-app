from application.orders.commands.checkout.checkout import CheckoutCommand


class CheckoutCommandValidator:
    def validate(self, request: CheckoutCommand) -> None:
        """No client fields. Authentication and ownership are checked inside the handler."""
