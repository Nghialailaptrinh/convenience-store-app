from dataclasses import dataclass
from decimal import Decimal

from domain.exceptions.business_rule_error import BusinessRuleError


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "VND"

    def __post_init__(self) -> None:
        if not isinstance(self.amount, Decimal) or not self.amount.is_finite() or self.amount < 0:
            raise BusinessRuleError("Số tiền phải là Decimal hữu hạn và không âm.")
        if self.currency != "VND" or self.amount != self.amount.to_integral_value():
            raise BusinessRuleError("Demo chỉ hỗ trợ số tiền nguyên VND.")

    def multiply(self, quantity: int) -> "Money":
        return Money(self.amount * quantity, self.currency)
