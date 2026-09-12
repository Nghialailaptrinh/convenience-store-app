from decimal import Decimal

import pytest

from domain.exceptions.business_rule_error import BusinessRuleError
from domain.value_objects.money import Money


@pytest.mark.parametrize(
    "amount", [Decimal(-1), Decimal("NaN"), Decimal("Infinity"), Decimal("1.5"), 1.0]
)
def test_invalid_money(amount):
    with pytest.raises(BusinessRuleError):
        Money(amount)
