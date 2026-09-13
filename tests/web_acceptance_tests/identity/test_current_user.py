import pytest
from fastapi.testclient import TestClient

from web.program import create_app

PASSWORD = "a sufficiently long password"


def login(client, email):
    account = {"email": email, "password": PASSWORD}
    assert client.post("/identity/register", json=account).status_code == 201
    result = client.post("/identity/login", json=account)
    assert result.status_code == 200
    return result.json()


def test_two_users_are_request_scoped_and_token_survives_restart(tmp_path):
    database = f"sqlite:///{tmp_path / 'users.db'}"
    with TestClient(create_app(database)) as client:
        first, second = login(client, "a@example.com"), login(client, "b@example.com")
        for user, email in [
            (first, "a@example.com"),
            (second, "b@example.com"),
            (first, "a@example.com"),
        ]:
            response = client.get(
                "/identity/me", headers={"Authorization": f"Bearer {user['access_token']}"}
            )
            assert response.status_code == 200
            assert response.json() == {"user_id": user["user_id"], "email": email}
            assert response.headers["cache-control"] == "no-store"
        assert client.get("/identity/me").status_code == 401
        schema = client.get("/openapi.json").json()
        assert schema["paths"]["/identity/me"]["get"]["security"] == [{"HTTPBearer": []}]
    with TestClient(create_app(database)) as client:
        assert (
            client.get(
                "/identity/me", headers={"Authorization": f"Bearer {first['access_token']}"}
            ).status_code
            == 200
        )


@pytest.mark.parametrize(
    "header", [None, "Basic abc", "Bearer", "Bearer invalid", "Bearer " + "x" * 43]
)
def test_missing_malformed_or_unknown_token_returns_401(tmp_path, header):
    with TestClient(create_app(f"sqlite:///{tmp_path / 'invalid.db'}")) as client:
        response = client.get("/identity/me", headers={"Authorization": header} if header else {})
        assert response.status_code == 401
        assert response.headers["www-authenticate"] == "Bearer"
        assert response.json() == {"detail": "Authentication required"}
        assert client.get("/products").status_code == 200


def test_tampered_and_expired_tokens_fail_at_http_boundary(tmp_path):
    with TestClient(create_app(f"sqlite:///{tmp_path / 'expiry.db'}")) as client:
        user = login(client, "a@example.com")
        token = user["access_token"]
        changed = ("A" if token[0] != "A" else "B") + token[1:]
        assert (
            client.get("/identity/me", headers={"Authorization": f"Bearer {changed}"}).status_code
            == 401
        )
        tokens = client.app.state.tokens
        original_clock = tokens._clock
        tokens._clock = lambda: original_clock() + 3601
        assert (
            client.get("/identity/me", headers={"Authorization": f"Bearer {token}"}).status_code
            == 401
        )
