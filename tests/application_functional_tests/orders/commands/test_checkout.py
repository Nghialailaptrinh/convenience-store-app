from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace
from uuid import UUID

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from application.carts.commands.add_product_to_cart.add_product_to_cart import (
    AddProductToCartCommand,
    AddProductToCartCommandHandler,
)
from application.carts.queries.get_cart.get_cart import GetCartQuery, GetCartQueryHandler
from application.common.exceptions.payment_failed import PaymentFailedError
from application.orders.commands.checkout.checkout import CheckoutCommand, CheckoutCommandHandler
from domain.exceptions.business_rule_error import BusinessRuleError
from infrastructure.data.configurations.order_configuration import OrderRecord
from infrastructure.data.configurations.product_configuration import ProductRecord
from infrastructure.dependency_injection import create_demo_dependencies, create_identity_service
from infrastructure.payment.fake_payment_gateway import FakePaymentGateway


@pytest.fixture
def dependencies(tmp_path):
    engine, factory, payment = create_demo_dependencies(f"sqlite:///{tmp_path / 'app.db'}")
    _, user_id = create_identity_service(engine).create_user(
        "a@example.com", "a sufficiently long password"
    )
    yield engine, factory, payment, SimpleNamespace(user_id=user_id)
    engine.dispose()


def test_failed_payment_rolls_back_cart_and_order(dependencies):
    engine, factory, _, user = dependencies
    AddProductToCartCommandHandler(factory(), user).handle(AddProductToCartCommand(UUID(int=1), 2))
    with pytest.raises(PaymentFailedError):
        CheckoutCommandHandler(factory(), FakePaymentGateway(fail=True), user).handle(
            CheckoutCommand()
        )
    assert GetCartQueryHandler(factory(), user).handle(GetCartQuery()).items[0].quantity == 2
    with Session(engine) as session:
        assert session.scalar(select(func.count()).select_from(OrderRecord)) == 0


def test_concurrent_checkout_consumes_cart_once(dependencies):
    engine, factory, payment, user = dependencies
    AddProductToCartCommandHandler(factory(), user).handle(AddProductToCartCommand(UUID(int=1), 2))

    def attempt():
        try:
            return CheckoutCommandHandler(factory(), payment, user).handle(CheckoutCommand())
        except BusinessRuleError:
            return None

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: attempt(), range(2)))
    assert sum(result is not None for result in results) == 1
    with Session(engine) as session:
        assert session.scalar(select(func.count()).select_from(OrderRecord)) == 1


def test_inactive_product_rejected_without_consuming_cart(dependencies):
    engine, factory, payment, user = dependencies
    AddProductToCartCommandHandler(factory(), user).handle(AddProductToCartCommand(UUID(int=1), 2))
    with Session(engine) as session, session.begin():
        session.get(ProductRecord, str(UUID(int=1))).is_active = False
    with pytest.raises(BusinessRuleError):
        CheckoutCommandHandler(factory(), payment, user).handle(CheckoutCommand())
    assert GetCartQueryHandler(factory(), user).handle(GetCartQuery()).items[0].quantity == 2
