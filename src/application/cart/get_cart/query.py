from dataclasses import dataclass
from uuid import UUID

from application.errors import UseCaseNotImplemented
from domain.entities.cart import Cart


@dataclass(frozen=True)
class GetCartQuery:
    customer_id: UUID


def handle(query: GetCartQuery) -> Cart | None:
    raise UseCaseNotImplemented("TODO: implement GetCart query")
