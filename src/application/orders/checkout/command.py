from dataclasses import dataclass
from uuid import UUID

from application.errors import UseCaseNotImplemented


@dataclass(frozen=True)
class CheckoutCommand:
    customer_id: UUID


def handle(command: CheckoutCommand) -> UUID:
    raise UseCaseNotImplemented("TODO: implement Checkout command")
