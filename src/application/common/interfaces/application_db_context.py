from typing import Protocol, Self

from application.common.interfaces.cart_repository import ICartRepository
from application.common.interfaces.customer_repository import ICustomerRepository
from application.common.interfaces.order_repository import IOrderRepository
from application.common.interfaces.product_repository import IProductRepository


class IApplicationDbContext(Protocol):
    customers: ICustomerRepository
    products: IProductRepository
    carts: ICartRepository
    orders: IOrderRepository

    def __enter__(self) -> Self: ...

    def __exit__(self, exc_type, exc_value, traceback) -> None: ...

    def save_changes(self) -> None: ...
