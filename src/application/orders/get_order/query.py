from dataclasses import dataclass
from uuid import UUID

from application.errors import UseCaseNotImplemented
from domain.entities.order import Order


@dataclass(frozen=True)
class GetOrderQuery:
    order_id: UUID


def handle(query: GetOrderQuery) -> Order | None:
    raise UseCaseNotImplemented("TODO: implement GetOrder query")
