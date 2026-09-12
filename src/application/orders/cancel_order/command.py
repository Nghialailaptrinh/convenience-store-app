from dataclasses import dataclass
from uuid import UUID

from application.errors import UseCaseNotImplemented


@dataclass(frozen=True)
class CancelOrderCommand:
    order_id: UUID


def handle(command: CancelOrderCommand) -> None:
    raise UseCaseNotImplemented("TODO: implement CancelOrder command")
