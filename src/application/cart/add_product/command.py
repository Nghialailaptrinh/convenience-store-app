from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class AddProductToCartCommand:
    customer_id: UUID
    product_id: UUID
    quantity: int


def handle(command: AddProductToCartCommand) -> None:
    raise NotImplementedError("TODO: implement AddProductToCart command")
