from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class RemoveProductFromCartCommand:
    customer_id: UUID
    product_id: UUID


def handle(command: RemoveProductFromCartCommand) -> None:
    raise NotImplementedError("TODO: implement RemoveProductFromCart command")
