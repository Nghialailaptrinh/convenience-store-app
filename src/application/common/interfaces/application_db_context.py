from typing import Protocol, Self

from application.common.interfaces.cart_repository import CartRepository
from application.common.interfaces.order_repository import OrderRepository
from application.common.interfaces.product_repository import ProductRepository


class ApplicationDbContext(Protocol):
    products: ProductRepository
    carts: CartRepository
    orders: OrderRepository

    def __enter__(self) -> Self: ...

    def __exit__(self, exc_type, exc_value, traceback) -> None: ...

    def save_changes(self) -> None: ...
