from typing import Annotated

from fastapi import Depends, Request

from application.common.interfaces.payment_gateway import PaymentGateway
from application.common.interfaces.unit_of_work import UnitOfWork


def get_unit_of_work(request: Request) -> UnitOfWork:
    return request.app.state.uow_factory()


def get_payment_gateway(request: Request) -> PaymentGateway:
    return request.app.state.payment


UowDependency = Annotated[UnitOfWork, Depends(get_unit_of_work)]
PaymentDependency = Annotated[PaymentGateway, Depends(get_payment_gateway)]
