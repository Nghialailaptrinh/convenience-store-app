from dataclasses import dataclass
from uuid import UUID

from application.common.exceptions.use_case_not_implemented import UseCaseNotImplemented


@dataclass(frozen=True)
class CreateOrderCommand:
    customer_id: UUID


def handle(command: CreateOrderCommand) -> UUID:
    raise UseCaseNotImplemented("TODO: implement CreateOrder command")
