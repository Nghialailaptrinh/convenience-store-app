from dataclasses import dataclass
from decimal import Decimal

from domain.value_objects.money import Money


@dataclass(frozen=True)
class MoneyDto:
    amount: Decimal
    currency: str

    @classmethod
    def from_domain(cls, value: Money) -> "MoneyDto":
        return cls(value.amount, value.currency)
