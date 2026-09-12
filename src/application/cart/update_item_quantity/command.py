from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UpdateCartItemQuantityCommand:
    customer_id: UUID
    product_id: UUID
    quantity: int


def handle(command: UpdateCartItemQuantityCommand) -> None:
    raise NotImplementedError("TODO: implement UpdateCartItemQuantity command")
