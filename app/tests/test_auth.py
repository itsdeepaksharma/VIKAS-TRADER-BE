from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

REGISTER_PAYLOAD = {
    "first_name": "Test",
    "last_name": "User",
    "email": "test.user@example.com",
    "phone": "9876543210",
    "address": "42 Test Street, Ludhiana, Punjab 141003",
    "password": "securepass123",
}


def test_register_and_login_flow() -> None:
    register_response = client.post("/api/v1/auth/register", json=REGISTER_PAYLOAD)
    assert register_response.status_code == 201
    register_data = register_response.json()
    assert register_data["access_token"]
    assert register_data["user"]["email"] == REGISTER_PAYLOAD["email"]

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": REGISTER_PAYLOAD["email"],
            "password": REGISTER_PAYLOAD["password"],
        },
    )
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert login_data["access_token"]
    assert login_data["user"]["first_name"] == "Test"
