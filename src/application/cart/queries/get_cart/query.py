from dataclasses import dataclass
from uuid import UUID

from application.common.exceptions.use_case_not_implemented import UseCaseNotImplemented
from domain.entities.cart import Cart


@dataclass(frozen=True)
class GetCartQuery:
    customer_id: UUID


def handle(query: GetCartQuery) -> Cart | None:
    raise UseCaseNotImplemented("TODO: implement GetCart query")
