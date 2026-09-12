from concurrent.futures import ThreadPoolExecutor
from uuid import UUID, uuid4

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
from infrastructure.dependency_injection import create_demo_dependencies
from infrastructure.payment.fake_payment_gateway import FakePaymentGateway


@pytest.fixture
def dependencies(tmp_path):
    engine, factory, payment = create_demo_dependencies(f"sqlite:///{tmp_path / 'app.db'}")
    yield engine, factory, payment
    engine.dispose()


def test_failed_payment_rolls_back_cart_and_order(dependencies):
    engine, factory, _ = dependencies
    customer = uuid4()
    AddProductToCartCommandHandler(factory()).handle(
        AddProductToCartCommand(customer, UUID(int=1), 2)
    )
    with pytest.raises(PaymentFailedError):
        CheckoutCommandHandler(factory(), FakePaymentGateway(fail=True)).handle(
            CheckoutCommand(customer)
        )
    assert GetCartQueryHandler(factory()).handle(GetCartQuery(customer)).items[0].quantity == 2
    with Session(engine) as session:
        assert session.scalar(select(func.count()).select_from(OrderRecord)) == 0


def test_concurrent_checkout_consumes_cart_once(dependencies):
    engine, factory, payment = dependencies
    customer = uuid4()
    AddProductToCartCommandHandler(factory()).handle(
        AddProductToCartCommand(customer, UUID(int=1), 2)
    )

    def attempt():
        try:
            return CheckoutCommandHandler(factory(), payment).handle(CheckoutCommand(customer))
        except BusinessRuleError:
            return None

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: attempt(), range(2)))
    assert sum(result is not None for result in results) == 1
    with Session(engine) as session:
        assert session.scalar(select(func.count()).select_from(OrderRecord)) == 1


def test_inactive_product_rejected_without_consuming_cart(dependencies):
    engine, factory, payment = dependencies
    customer = uuid4()
    AddProductToCartCommandHandler(factory()).handle(
        AddProductToCartCommand(customer, UUID(int=1), 2)
    )
    with Session(engine) as session, session.begin():
        session.get(ProductRecord, str(UUID(int=1))).is_active = False
    with pytest.raises(BusinessRuleError):
        CheckoutCommandHandler(factory(), payment).handle(CheckoutCommand(customer))
    assert GetCartQueryHandler(factory()).handle(GetCartQuery(customer)).items[0].quantity == 2
