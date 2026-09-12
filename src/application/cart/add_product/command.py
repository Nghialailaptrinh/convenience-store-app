from dataclasses import dataclass
from uuid import UUID

from application.errors import UseCaseNotImplemented


@dataclass(frozen=True)
class AddProductToCartCommand:
    customer_id: UUID
    product_id: UUID
    quantity: int


def handle(command: AddProductToCartCommand) -> None:
    raise UseCaseNotImplemented("TODO: implement AddProductToCart command")
