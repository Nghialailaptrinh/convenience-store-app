from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from web.program import create_app


@pytest.fixture
def shop(tmp_path):
    with TestClient(create_app(f"sqlite:///{tmp_path / 'ownership.db'}")) as client:
        yield client


def account(shop, email):
    body = {"email": email, "password": "a sufficiently long password"}
    assert shop.post("/identity/register", json=body).status_code == 201
    response = shop.post("/identity/login", json=body).json()
    return {"Authorization": f"Bearer {response['access_token']}"}, response["user_id"]


def test_two_accounts_have_separate_carts_history_and_order_permissions(shop):
    first, first_id = account(shop, "a@example.com")
    second, _ = account(shop, "b@example.com")
    product = shop.get("/products").json()[0]["id"]
    assert (
        shop.post(
            "/cart/items", headers=first, json={"product_id": product, "quantity": 2}
        ).status_code
        == 204
    )
    first_cart = shop.get("/cart", headers=first).json()
    assert first_cart["customer_id"] != first_id
    assert shop.get("/cart", headers=second).json()["items"] == []
    assert (
        shop.get(f"/cart?customer_id={first_cart['customer_id']}", headers=second).json()["items"]
        == []
    )
    for method, path, body in [
        (
            "post",
            "/cart/items",
            {"product_id": product, "quantity": 1, "customer_id": first_cart["customer_id"]},
        ),
        (
            "patch",
            f"/cart/items/{product}",
            {"quantity": 9, "customer_id": first_cart["customer_id"]},
        ),
        ("post", "/orders", {"customer_id": first_cart["customer_id"]}),
        ("post", "/orders/checkout", {"customer_id": first_cart["customer_id"]}),
    ]:
        assert getattr(shop, method)(path, headers=second, json=body).status_code == 422
    assert (
        shop.delete(
            f"/cart/items/{product}?customer_id={first_cart['customer_id']}", headers=second
        ).status_code
        == 204
    )
    assert shop.get("/cart", headers=first).json()["items"][0]["quantity"] == 2
    pending = shop.post("/orders", headers=first, json={}).json()["order_id"]
    assert shop.get("/orders/me", headers=second).json() == []
    assert [row["id"] for row in shop.get("/orders/me", headers=first).json()] == [pending]
    assert shop.get(f"/orders/{pending}", headers=second).status_code == 404
    assert shop.post(f"/orders/{pending}/cancel", headers=second).status_code == 404
    assert shop.get(f"/orders/{pending}", headers=first).json()["status"] == "pending"
    assert shop.post(f"/orders/{pending}/cancel", headers=first).status_code == 204
    assert (
        shop.post(
            "/cart/items", headers=second, json={"product_id": product, "quantity": 1}
        ).status_code
        == 204
    )
    paid = shop.post("/orders/checkout", headers=second, json={}).json()["order_id"]
    assert shop.get(f"/orders/{paid}", headers=second).json()["status"] == "paid"
    assert shop.get(f"/orders/{paid}", headers=first).status_code == 404
    assert [row["id"] for row in shop.get("/orders/me", headers=second).json()] == [paid]


@pytest.mark.parametrize(
    "method,path,body",
    [
        ("get", "/cart", None),
        ("post", "/cart/items", {"product_id": str(uuid4()), "quantity": 1}),
        ("patch", f"/cart/items/{uuid4()}", {"quantity": 1}),
        ("delete", f"/cart/items/{uuid4()}", None),
        ("post", "/orders", {}),
        ("post", "/orders/checkout", {}),
        ("get", "/orders/me", None),
        ("get", f"/orders/{uuid4()}", None),
        ("post", f"/orders/{uuid4()}/cancel", None),
    ],
)
def test_shopping_requires_authentication(shop, method, path, body):
    response = shop.request(method, path, json=body)
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
