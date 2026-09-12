from dataclasses import dataclass
from uuid import UUID

from application.errors import UseCaseNotImplemented


@dataclass(frozen=True)
class RemoveProductFromCartCommand:
    customer_id: UUID
    product_id: UUID


def handle(command: RemoveProductFromCartCommand) -> None:
    raise UseCaseNotImplemented("TODO: implement RemoveProductFromCart command")
