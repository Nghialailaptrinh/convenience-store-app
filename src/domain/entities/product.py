from dataclasses import dataclass
from uuid import UUID

from domain.value_objects.money import Money


@dataclass
class Product:
    id: UUID
    name: str
    description: str
    price: Money
    category_id: UUID
    is_active: bool = True
