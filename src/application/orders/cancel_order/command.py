from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CancelOrderCommand:
    order_id: UUID


def handle(command: CancelOrderCommand) -> None:
    raise NotImplementedError("TODO: implement CancelOrder command")
