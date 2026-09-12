from uuid import UUID

from pydantic import BaseModel

from web.schemas.product import MoneyResponse


class CheckoutRequest(BaseModel):
    customer_id: UUID


class CreateOrderRequest(BaseModel):
    customer_id: UUID


class OrderCreatedResponse(BaseModel):
    order_id: UUID


class OrderItemResponse(BaseModel):
    product_id: UUID
    quantity: int
    unit_price: MoneyResponse
    product_name: str


class OrderResponse(BaseModel):
    id: UUID
    customer_id: UUID
    status: str
    items: list[OrderItemResponse]
    total: MoneyResponse
    payment_reference: str | None = None
