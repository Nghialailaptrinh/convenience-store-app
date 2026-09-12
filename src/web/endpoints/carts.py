from uuid import UUID

from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, Field

from application.carts.commands.add_product_to_cart.add_product_to_cart import (
    AddProductToCartCommand,
)
from application.carts.commands.remove_product_from_cart.remove_product_from_cart import (
    RemoveProductFromCartCommand,
)
from application.carts.commands.update_cart_item_quantity.update_cart_item_quantity import (
    UpdateCartItemQuantityCommand,
)
from application.carts.queries.get_cart.cart_dto import CartDto
from application.carts.queries.get_cart.get_cart import GetCartQuery
from web.dependency_injection import SenderDependency


class AddProductToCartRequest(BaseModel):
    customer_id: UUID
    product_id: UUID
    quantity: int = Field(gt=0, le=99, strict=True)


class UpdateCartItemQuantityRequest(BaseModel):
    customer_id: UUID
    quantity: int = Field(gt=0, le=99, strict=True)


router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("", response_model=CartDto)
def get_cart(customer_id: UUID, sender: SenderDependency):
    result = sender.send(GetCartQuery(customer_id))
    if result is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return result


@router.post("/items", status_code=204)
def add_product_to_cart(request: AddProductToCartRequest, sender: SenderDependency) -> Response:
    sender.send(AddProductToCartCommand(**request.model_dump()))
    return Response(status_code=204)


@router.delete("/items/{product_id}", status_code=204)
def remove_product_from_cart(
    product_id: UUID, customer_id: UUID, sender: SenderDependency
) -> Response:
    sender.send(RemoveProductFromCartCommand(customer_id, product_id))
    return Response(status_code=204)


@router.patch("/items/{product_id}", status_code=204)
def update_cart_item_quantity(
    product_id: UUID, request: UpdateCartItemQuantityRequest, sender: SenderDependency
) -> Response:
    sender.send(
        UpdateCartItemQuantityCommand(
            request.customer_id,
            product_id,
            request.quantity,
        )
    )
    return Response(status_code=204)
