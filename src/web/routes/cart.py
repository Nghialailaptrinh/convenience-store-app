from uuid import UUID

from fastapi import APIRouter, HTTPException, Response

from application.cart.add_product import command as add_slice
from application.cart.get_cart import query as get_slice
from application.cart.remove_product import command as remove_slice
from application.cart.update_item_quantity import command as update_slice
from web.schemas.cart import (
    AddProductToCartRequest,
    CartResponse,
    UpdateCartItemQuantityRequest,
)

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("", response_model=CartResponse)
def get_cart(customer_id: UUID):
    result = get_slice.handle(get_slice.GetCartQuery(customer_id))
    if result is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return result


@router.post("/items", status_code=204)
def add_product_to_cart(request: AddProductToCartRequest) -> Response:
    add_slice.handle(add_slice.AddProductToCartCommand(**request.model_dump()))
    return Response(status_code=204)


@router.delete("/items/{product_id}", status_code=204)
def remove_product_from_cart(product_id: UUID, customer_id: UUID) -> Response:
    remove_slice.handle(remove_slice.RemoveProductFromCartCommand(customer_id, product_id))
    return Response(status_code=204)


@router.patch("/items/{product_id}", status_code=204)
def update_cart_item_quantity(product_id: UUID, request: UpdateCartItemQuantityRequest) -> Response:
    update_slice.handle(update_slice.UpdateCartItemQuantityCommand(
        request.customer_id, product_id, request.quantity,
    ))
    return Response(status_code=204)
