from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CheckoutCommand:
    customer_id: UUID


def handle(command: CheckoutCommand) -> UUID:
    raise NotImplementedError("TODO: implement Checkout command")
