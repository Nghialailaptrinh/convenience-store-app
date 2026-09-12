from dataclasses import dataclass
from uuid import UUID

from application.common.exceptions.use_case_not_implemented import UseCaseNotImplemented


@dataclass(frozen=True)
class CancelOrderCommand:
    order_id: UUID


def handle(command: CancelOrderCommand) -> None:
    raise UseCaseNotImplemented("TODO: implement CancelOrder command")
