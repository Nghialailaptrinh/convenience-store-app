from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from web.program import create_app


def authenticate(client):
    account = {"email": "shopper@example.com", "password": "a sufficiently long password"}
    client.post("/identity/register", json=account)
    token = client.post("/identity/login", json=account).json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"


@pytest.fixture
def client(tmp_path):
    with TestClient(create_app(f"sqlite:///{tmp_path / 'test.db'}")) as client:
        authenticate(client)
        yield client


def add(client, customer, product, quantity=1):
    return client.post(
        "/cart/items",
        json={
            "product_id": product,
            "quantity": quantity,
        },
    )


def test_storefront_and_catalog(client):
    assert client.get("/").status_code == 200
    assert client.get("/static/app.js").status_code == 200
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/openapi.json").status_code == 200
    products = client.get("/products").json()
    assert len(products) == 9
    assert client.get(f"/products/{products[0]['id']}").json() == products[0]
    assert client.get(f"/products/{uuid4()}").status_code == 404


def test_cart_order_and_cancel(client):
    customer = str(uuid4())
    product = client.get("/products").json()[0]
    url = f"/cart?customer_id={customer}"
    assert client.get(url).json()["items"] == []
    assert add(client, customer, product["id"], 2).status_code == 204
    assert add(client, customer, product["id"]).status_code == 204
    assert client.get(url).json()["items"][0]["quantity"] == 3
    assert (
        client.patch(
            f"/cart/items/{product['id']}",
            json={
                "quantity": 4,
            },
        ).status_code
        == 204
    )
    result = client.post("/orders", json={})
    assert result.status_code == 201, result.text
    order_url = f"/orders/{result.json()['order_id']}"
    order = client.get(order_url).json()
    assert order["status"] == "pending"
    assert int(order["total"]["amount"]) == int(product["price"]["amount"]) * 4
    assert order["items"][0]["product_name"] == product["name"]
    assert client.get(url).json()["items"] == []
    assert client.post(order_url + "/cancel").status_code == 204
    assert client.post(order_url + "/cancel").status_code == 204
    assert client.get(order_url).json()["status"] == "cancelled"


def test_checkout_and_invalid_transitions(client):
    customer = str(uuid4())
    product = client.get("/products").json()[0]["id"]
    assert client.post("/orders/checkout", json={}).status_code == 409
    add(client, customer, product)
    result = client.post("/orders/checkout", json={})
    assert result.status_code == 201, result.text
    url = f"/orders/{result.json()['order_id']}"
    assert client.get(url).json()["status"] == "paid"
    assert client.get(url).json()["payment_reference"].startswith("demo-")
    assert client.post(url + "/cancel").status_code == 409
    assert client.post("/orders/checkout", json={}).status_code == 409


def test_remove_validation_and_customer_separation(client):
    customer = str(uuid4())
    product = client.get("/products").json()[0]["id"]
    for quantity in [0, -1, 100, True, 1.5]:
        assert add(client, customer, product, quantity).status_code == 422
    assert add(client, customer, str(uuid4())).status_code == 404
    assert client.get("/products/not-a-uuid").status_code == 422
    add(client, customer, product)
    assert (
        len(client.get(f"/cart?customer_id={uuid4()}").json()["items"]) == 1
    )  # Cannot select another owner.
    assert client.delete(f"/cart/items/{product}?customer_id={customer}").status_code == 204
    assert client.get(f"/cart?customer_id={customer}").json()["items"] == []
    assert client.get(f"/orders/{uuid4()}").status_code == 404


def test_database_survives_app_restart(tmp_path):
    url = f"sqlite:///{tmp_path / 'persistent.db'}"
    customer = str(uuid4())
    with TestClient(create_app(url)) as first:
        authenticate(first)
        product = first.get("/products").json()[0]["id"]
        add(first, customer, product, 2)
        order = first.post("/orders", json={}).json()["order_id"]
        add(first, customer, product, 3)
    with TestClient(create_app(url)) as second:
        authenticate(second)
        assert len(second.get("/products").json()) == 9
        assert second.get(f"/cart?customer_id={customer}").json()["items"][0]["quantity"] == 3
        assert second.get(f"/orders/{order}").json()["status"] == "pending"
