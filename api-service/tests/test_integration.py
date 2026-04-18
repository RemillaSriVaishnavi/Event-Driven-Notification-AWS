from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_user_register_flow():
    response = client.post("/api/users/register", json={
        "user_id": "u123",
        "email": "test@test.com"
    })

    assert response.status_code == 200