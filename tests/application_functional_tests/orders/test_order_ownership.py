from types import SimpleNamespace
from uuid import UUID

import pytest
from sqlalchemy import event

from application.carts.commands.add_product_to_cart.add_product_to_cart import (
    AddProductToCartCommand,
)
from application.carts.queries.get_cart.get_cart import GetCartQuery
from application.common.exceptions.not_found import NotFoundError
from application.common.exceptions.unauthenticated import UnauthenticatedError
from application.dependency_injection import create_sender
from application.orders.commands.cancel_order.cancel_order import CancelOrderCommand
from application.orders.commands.create_order.create_order import CreateOrderCommand
from application.orders.queries.get_my_orders.get_my_orders import GetMyOrdersQuery
from application.orders.queries.get_order.get_order import GetOrderQuery
from infrastructure.dependency_injection import create_demo_dependencies, create_identity_service


def test_ownership_is_enforced_in_application_without_http(tmp_path):
    engine, contexts, payment = create_demo_dependencies(f"sqlite:///{tmp_path / 'application.db'}")
    try:
        identity = create_identity_service(engine)
        _, a = identity.create_user("a@example.com", "a sufficiently long password")
        _, b = identity.create_user("b@example.com", "a sufficiently long password")
        first = create_sender(contexts, payment, current_user=SimpleNamespace(user_id=a))
        second = create_sender(contexts, payment, current_user=SimpleNamespace(user_id=b))
        guest = create_sender(contexts, payment)
        with pytest.raises(UnauthenticatedError):
            guest.send(GetCartQuery())
        first.send(AddProductToCartCommand(UUID(int=1), 2))
        assert second.send(GetCartQuery()).items == []
        order_id = first.send(CreateOrderCommand())
        commits = []
        event.listen(engine, "commit", lambda connection: commits.append(True))
        assert second.send(GetOrderQuery(order_id)) is None
        with pytest.raises(NotFoundError):
            second.send(CancelOrderCommand(order_id))
        assert second.send(GetMyOrdersQuery()) == []
        assert first.send(GetMyOrdersQuery())[0].id == order_id
        assert first.send(GetOrderQuery(order_id)).status == "pending"
        assert commits == []
        first.send(CancelOrderCommand(order_id))
        assert len(commits) == 1
    finally:
        engine.dispose()
