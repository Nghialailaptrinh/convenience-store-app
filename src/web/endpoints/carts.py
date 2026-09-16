from uuid import UUID

from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, ConfigDict, Field

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
from web.dependency_injection import AuthenticatedSenderDependency


class AddProductToCartRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    product_id: UUID
    quantity: int = Field(gt=0, le=99, strict=True)


class UpdateCartItemQuantityRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    quantity: int = Field(gt=0, le=99, strict=True)


router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("", response_model=CartDto)
def get_cart(sender: AuthenticatedSenderDependency):
    result = sender.send(GetCartQuery())
    if result is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return result


@router.post("/items", status_code=204)
def add_product_to_cart(
    request: AddProductToCartRequest, sender: AuthenticatedSenderDependency
) -> Response:
    sender.send(AddProductToCartCommand(**request.model_dump()))
    return Response(status_code=204)


@router.delete("/items/{product_id}", status_code=204)
def remove_product_from_cart(product_id: UUID, sender: AuthenticatedSenderDependency) -> Response:
    sender.send(RemoveProductFromCartCommand(product_id))
    return Response(status_code=204)


@router.patch("/items/{product_id}", status_code=204)
def update_cart_item_quantity(
    product_id: UUID, request: UpdateCartItemQuantityRequest, sender: AuthenticatedSenderDependency
) -> Response:
    sender.send(
        UpdateCartItemQuantityCommand(
            product_id,
            request.quantity,
        )
    )
    return Response(status_code=204)
