from typing import Protocol
from uuid import UUID

from src.domain.value_objects.money import Money


class PaymentGateway(Protocol):
    def charge(self, customer_id: UUID, amount: Money) -> str: ...
