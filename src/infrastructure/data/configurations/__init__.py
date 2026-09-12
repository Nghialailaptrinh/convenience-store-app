"""Register all SQLAlchemy mappings before creating the demo database."""

from infrastructure.data.configurations.base import Base
from infrastructure.data.configurations.cart_configuration import CartRecord
from infrastructure.data.configurations.order_configuration import OrderRecord
from infrastructure.data.configurations.product_configuration import ProductRecord

__all__ = ["Base", "CartRecord", "OrderRecord", "ProductRecord"]
