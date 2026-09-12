from dataclasses import dataclass
from uuid import UUID

from domain.exceptions.business_rule_error import BusinessRuleError


@dataclass
class CartItem:
    product_id: UUID
    quantity: int

    def __post_init__(self) -> None:
        self.validate_quantity(self.quantity)

    @staticmethod
    def validate_quantity(quantity: int) -> None:
        if type(quantity) is not int or not 1 <= quantity <= 99:
            raise BusinessRuleError("Số lượng mỗi sản phẩm phải từ 1 đến 99.")
