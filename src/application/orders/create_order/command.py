from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateOrderCommand:
    customer_id: UUID


def handle(command: CreateOrderCommand) -> UUID:
    raise NotImplementedError("TODO: implement CreateOrder command")
