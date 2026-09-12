from uuid import UUID

from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel

from application.orders.commands.cancel_order.cancel_order import CancelOrderCommand
from application.orders.commands.checkout.checkout import CheckoutCommand
from application.orders.commands.create_order.create_order import CreateOrderCommand
from application.orders.queries.get_order.get_order import GetOrderQuery
from application.orders.queries.get_order.order_dto import OrderDto
from web.dependency_injection import SenderDependency


class CheckoutRequest(BaseModel):
    customer_id: UUID


class CreateOrderRequest(BaseModel):
    customer_id: UUID


class OrderCreatedResponse(BaseModel):
    order_id: UUID


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/checkout", response_model=OrderCreatedResponse, status_code=201)
def checkout(request: CheckoutRequest, sender: SenderDependency):
    order_id = sender.send(CheckoutCommand(request.customer_id))
    return OrderCreatedResponse(order_id=order_id)


@router.post("", response_model=OrderCreatedResponse, status_code=201)
def create_order(request: CreateOrderRequest, sender: SenderDependency):
    order_id = sender.send(CreateOrderCommand(request.customer_id))
    return OrderCreatedResponse(order_id=order_id)


@router.get("/{order_id}", response_model=OrderDto)
def get_order(order_id: UUID, sender: SenderDependency):
    result = sender.send(GetOrderQuery(order_id))
    if result is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return result


@router.post("/{order_id}/cancel", status_code=204)
def cancel_order(order_id: UUID, sender: SenderDependency) -> Response:
    sender.send(CancelOrderCommand(order_id))
    return Response(status_code=204)
