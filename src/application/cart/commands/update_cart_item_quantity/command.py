from dataclasses import dataclass
from uuid import UUID

from application.common.exceptions.use_case_not_implemented import UseCaseNotImplemented


@dataclass(frozen=True)
class UpdateCartItemQuantityCommand:
    customer_id: UUID
    product_id: UUID
    quantity: int


def handle(command: UpdateCartItemQuantityCommand) -> None:
    raise UseCaseNotImplemented("TODO: implement UpdateCartItemQuantity command")
