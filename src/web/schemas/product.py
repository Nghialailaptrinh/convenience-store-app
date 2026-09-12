from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class MoneyResponse(BaseModel):
    amount: Decimal
    currency: str


class ProductResponse(BaseModel):
    id: UUID
    name: str
    description: str
    price: MoneyResponse
    category_id: UUID
    is_active: bool
