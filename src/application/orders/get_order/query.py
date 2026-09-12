from dataclasses import dataclass
from uuid import UUID

from src.domain.entities.order import Order


@dataclass(frozen=True)
class GetOrderQuery:
    order_id: UUID


def handle(query: GetOrderQuery) -> Order | None:
    raise NotImplementedError("TODO: implement GetOrder query")
