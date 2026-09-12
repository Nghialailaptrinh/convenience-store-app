from dataclasses import dataclass
from uuid import UUID

from application.common.models.money_dto import MoneyDto
from domain.entities.product import Product


@dataclass(frozen=True)
class ProductDto:
    id: UUID
    name: str
    description: str
    price: MoneyDto
    category_id: UUID
    is_active: bool

    @classmethod
    def from_domain(cls, product: Product) -> "ProductDto":
        return cls(
            product.id,
            product.name,
            product.description,
            MoneyDto.from_domain(product.price),
            product.category_id,
            product.is_active,
        )
