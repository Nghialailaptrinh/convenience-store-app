from concurrent.futures import ThreadPoolExecutor
from uuid import UUID, uuid4

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from application.cart.commands.add_product_to_cart.command import AddProductToCartCommand
from application.cart.commands.add_product_to_cart.command import handle as add
from application.cart.queries.get_cart.query import GetCartQuery
from application.cart.queries.get_cart.query import handle as get_cart
from application.common.exceptions.payment_failed import PaymentFailedError
from application.orders.commands.checkout.command import CheckoutCommand
from application.orders.commands.checkout.command import handle as checkout
from domain.exceptions.business_rule_error import BusinessRuleError
from infrastructure.data.models import OrderRecord, ProductRecord
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
    add(AddProductToCartCommand(customer, UUID(int=1), 2), factory())
    with pytest.raises(PaymentFailedError):
        checkout(CheckoutCommand(customer), factory(), FakePaymentGateway(fail=True))
    assert get_cart(GetCartQuery(customer), factory()).items[0].quantity == 2
    with Session(engine) as session:
        assert session.scalar(select(func.count()).select_from(OrderRecord)) == 0


def test_concurrent_checkout_consumes_cart_once(dependencies):
    engine, factory, payment = dependencies
    customer = uuid4()
    add(AddProductToCartCommand(customer, UUID(int=1), 2), factory())
    def attempt():
        try:
            return checkout(CheckoutCommand(customer), factory(), payment)
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
    add(AddProductToCartCommand(customer, UUID(int=1), 2), factory())
    with Session(engine) as session, session.begin():
        session.get(ProductRecord, str(UUID(int=1))).is_active = False
    with pytest.raises(BusinessRuleError):
        checkout(CheckoutCommand(customer), factory(), payment)
    assert get_cart(GetCartQuery(customer), factory()).items[0].quantity == 2
