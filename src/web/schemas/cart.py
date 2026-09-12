from uuid import UUID

from pydantic import BaseModel, Field


class AddProductToCartRequest(BaseModel):
    customer_id: UUID
    product_id: UUID
    quantity: int = Field(gt=0)


class UpdateCartItemQuantityRequest(BaseModel):
    customer_id: UUID
    quantity: int = Field(gt=0)


class CartItemResponse(BaseModel):
    product_id: UUID
    quantity: int


class CartResponse(BaseModel):
    id: UUID
    customer_id: UUID
    items: list[CartItemResponse]
