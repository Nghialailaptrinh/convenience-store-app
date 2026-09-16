"""Register all SQLAlchemy mappings before creating the demo database."""

from infrastructure.data.configurations.access_token_configuration import AccessTokenRecord
from infrastructure.data.configurations.base import Base
from infrastructure.data.configurations.cart_configuration import CartRecord
from infrastructure.data.configurations.customer_configuration import CustomerRecord
from infrastructure.data.configurations.order_configuration import OrderRecord
from infrastructure.data.configurations.product_configuration import ProductRecord
from infrastructure.data.configurations.user_configuration import UserRecord

__all__ = [
    "AccessTokenRecord",
    "Base",
    "CartRecord",
    "CustomerRecord",
    "OrderRecord",
    "ProductRecord",
    "UserRecord",
]
