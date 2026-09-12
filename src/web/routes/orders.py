from uuid import UUID

from fastapi import APIRouter, HTTPException, Response

from application.orders.cancel_order import command as cancel_slice
from application.orders.checkout import command as checkout_slice
from application.orders.create_order import command as create_slice
from application.orders.get_order import query as get_slice
from web.schemas.order import (
    CheckoutRequest,
    CreateOrderRequest,
    OrderCreatedResponse,
    OrderResponse,
)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/checkout", response_model=OrderCreatedResponse, status_code=201)
def checkout(request: CheckoutRequest):
    order_id = checkout_slice.handle(checkout_slice.CheckoutCommand(request.customer_id))
    return OrderCreatedResponse(order_id=order_id)


@router.post("", response_model=OrderCreatedResponse, status_code=201)
def create_order(request: CreateOrderRequest):
    order_id = create_slice.handle(create_slice.CreateOrderCommand(request.customer_id))
    return OrderCreatedResponse(order_id=order_id)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: UUID):
    result = get_slice.handle(get_slice.GetOrderQuery(order_id))
    if result is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return result


@router.post("/{order_id}/cancel", status_code=204)
def cancel_order(order_id: UUID) -> Response:
    cancel_slice.handle(cancel_slice.CancelOrderCommand(order_id))
    return Response(status_code=204)
