from dataclasses import dataclass
from uuid import UUID

from src.domain.entities.cart import Cart


@dataclass(frozen=True)
class GetCartQuery:
    customer_id: UUID


def handle(query: GetCartQuery) -> Cart | None:
    raise NotImplementedError("TODO: implement GetCart query")
