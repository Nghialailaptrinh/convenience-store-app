from fastapi.testclient import TestClient

from web.program import create_app


def test_name_is_saved_trimmed_and_returned_after_login_and_restart(tmp_path):
    database = f"sqlite:///{tmp_path / 'name.db'}"
    name = "Nguy\u1ec5n V\u0103n An"
    account = {"email": "an@example.com", "password": "a sufficiently long password"}
    with TestClient(create_app(database)) as client:
        for invalid in ["   ", "x" * 101, 123]:
            response = client.post("/identity/register", json={**account, "name": invalid})
            assert response.status_code == 422
        assert (
            client.post("/identity/register", json={**account, "name": f"  {name}  "}).status_code
            == 201
        )
    with TestClient(create_app(database)) as client:
        login = client.post("/identity/login", json=account)
        assert login.status_code == 200
        response = client.get(
            "/identity/me", headers={"Authorization": f"Bearer {login.json()['access_token']}"}
        )
        assert response.status_code == 200
        assert response.json()["name"] == name
        assert response.json()["email"] == account["email"]
