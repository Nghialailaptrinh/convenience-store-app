from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass
class Product:
    id: UUID
    name: str
    description: str
    price: Decimal
    category_id: UUID
    is_active: bool = True
