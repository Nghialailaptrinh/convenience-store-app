from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from web.main import app

client = TestClient(app)
ID = str(uuid4())


def test_health_and_openapi():
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/openapi.json").status_code == 200


@pytest.mark.parametrize("method,path,body", [
    ("GET", "/products", None),
    ("GET", f"/products/{ID}", None),
    ("GET", f"/cart?customer_id={ID}", None),
    ("POST", "/cart/items", {"customer_id": ID, "product_id": ID, "quantity": 1}),
    ("DELETE", f"/cart/items/{ID}?customer_id={ID}", None),
    ("PATCH", f"/cart/items/{ID}", {"customer_id": ID, "quantity": 2}),
    ("POST", "/orders/checkout", {"customer_id": ID}),
    ("POST", "/orders", {"customer_id": ID}),
    ("GET", f"/orders/{ID}", None),
    ("POST", f"/orders/{ID}/cancel", None),
])
def test_unimplemented_use_cases_return_501(method, path, body):
    assert client.request(method, path, json=body).status_code == 501


def test_invalid_request_is_rejected():
    assert client.get("/products/not-a-uuid").status_code == 422
    response = client.post("/cart/items", json={
        "customer_id": ID, "product_id": ID, "quantity": 0,
    })
    assert response.status_code == 422
