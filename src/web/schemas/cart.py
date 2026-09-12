from uuid import UUID

from pydantic import BaseModel, Field


class AddProductToCartRequest(BaseModel):
    customer_id: UUID
    product_id: UUID
    quantity: int = Field(gt=0, le=99, strict=True)


class UpdateCartItemQuantityRequest(BaseModel):
    customer_id: UUID
    quantity: int = Field(gt=0, le=99, strict=True)


class CartItemResponse(BaseModel):
    product_id: UUID
    quantity: int


class CartResponse(BaseModel):
    id: UUID
    customer_id: UUID
    items: list[CartItemResponse]
