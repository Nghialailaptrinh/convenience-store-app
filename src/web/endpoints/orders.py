from uuid import UUID

from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, ConfigDict

from application.orders.commands.cancel_order.cancel_order import CancelOrderCommand
from application.orders.commands.checkout.checkout import CheckoutCommand
from application.orders.commands.create_order.create_order import CreateOrderCommand
from application.orders.queries.get_my_orders.get_my_orders import GetMyOrdersQuery
from application.orders.queries.get_order.get_order import GetOrderQuery
from application.orders.queries.get_order.order_dto import OrderDto
from web.dependency_injection import AuthenticatedSenderDependency


class CheckoutRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CreateOrderRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")


class OrderCreatedResponse(BaseModel):
    order_id: UUID


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/checkout", response_model=OrderCreatedResponse, status_code=201)
def checkout(request: CheckoutRequest, sender: AuthenticatedSenderDependency):
    order_id = sender.send(CheckoutCommand())
    return OrderCreatedResponse(order_id=order_id)


@router.post("", response_model=OrderCreatedResponse, status_code=201)
def create_order(request: CreateOrderRequest, sender: AuthenticatedSenderDependency):
    order_id = sender.send(CreateOrderCommand())
    return OrderCreatedResponse(order_id=order_id)


@router.get("/me", response_model=list[OrderDto])
def get_my_orders(sender: AuthenticatedSenderDependency):
    return sender.send(GetMyOrdersQuery())


@router.get("/{order_id}", response_model=OrderDto)
def get_order(order_id: UUID, sender: AuthenticatedSenderDependency):
    result = sender.send(GetOrderQuery(order_id))
    if result is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return result


@router.post("/{order_id}/cancel", status_code=204)
def cancel_order(order_id: UUID, sender: AuthenticatedSenderDependency) -> Response:
    sender.send(CancelOrderCommand(order_id))
    return Response(status_code=204)
