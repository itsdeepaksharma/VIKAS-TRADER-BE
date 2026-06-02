import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

REGISTER_TEMPLATE = {
    "first_name": "Test",
    "last_name": "User",
    "address": "42 Test Street, Ludhiana, Punjab 141003",
    "password": "securepass123",
}


def test_register_and_login_flow() -> None:
    suffix = uuid.uuid4().hex[:10]
    register_payload = {
        **REGISTER_TEMPLATE,
        "email": f"test.user.{suffix}@example.com",
        "phone": f"98{suffix[:8]}",
    }

    register_response = client.post("/api/v1/auth/register", json=register_payload)
    assert register_response.status_code == 201
    register_data = register_response.json()
    assert register_data["access_token"]
    assert register_data["user"]["email"] == register_payload["email"]

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": register_payload["email"],
            "password": register_payload["password"],
        },
    )
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert login_data["access_token"]
    assert login_data["user"]["first_name"] == "Test"
