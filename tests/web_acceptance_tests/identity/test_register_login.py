import pytest
from fastapi.testclient import TestClient

from web.program import create_app

ACCOUNT = {"email": "student@example.com", "password": "a sufficiently long password"}


@pytest.fixture
def client(tmp_path):
    with TestClient(create_app(f"sqlite:///{tmp_path / 'identity_http.db'}")) as client:
        yield client


def test_register_and_login_without_token_or_session(client):
    response = client.post("/identity/register", json=ACCOUNT)
    assert response.status_code == 201
    assert set(response.json()) == {"user_id"}
    login = client.post("/identity/login", json=ACCOUNT)
    assert login.status_code == 200
    assert login.json() == response.json()
    assert login.headers["cache-control"] == "no-store"
    assert "set-cookie" not in login.headers
    assert "access_token" not in login.json()
    assert ACCOUNT["password"] not in login.text
    assert client.get("/identity/me").status_code == 404


def test_duplicate_email_and_invalid_credentials(client):
    assert client.post("/identity/register", json=ACCOUNT).status_code == 201
    duplicate = client.post("/identity/register", json={**ACCOUNT, "email": "STUDENT@EXAMPLE.COM"})
    assert duplicate.status_code == 409
    wrong = client.post("/identity/login", json={**ACCOUNT, "password": "wrong password"})
    missing = client.post("/identity/login", json={**ACCOUNT, "email": "missing@example.com"})
    assert wrong.status_code == missing.status_code == 401
    assert wrong.json() == missing.json() == {"detail": "Invalid email or password"}


@pytest.mark.parametrize(
    "path,body",
    [
        ("register", {**ACCOUNT, "password": "short"}),
        ("register", {**ACCOUNT, "email": "invalid"}),
        ("register", {**ACCOUNT, "password": "secret" * 30}),
        ("login", {**ACCOUNT, "password": {"secret": "private-value"}}),
        ("login", {**ACCOUNT, "extra": "private-value"}),
        ("login", {**ACCOUNT, "password": ""}),
    ],
)
def test_invalid_requests_do_not_echo_secrets(client, path, body):
    response = client.post(f"/identity/{path}", json=body)
    assert response.status_code == 422
    assert ACCOUNT["password"] not in response.text
    assert "private-value" not in response.text
    assert '"input"' not in response.text


def test_identity_endpoints_appear_in_openapi(client):
    schema = client.get("/openapi.json").json()
    assert "/identity/register" in schema["paths"]
    assert "No token or session" in schema["paths"]["/identity/login"]["post"]["description"]
    password = schema["components"]["schemas"]["LoginUserRequest"]["properties"]["password"]
    assert password["writeOnly"] is True
