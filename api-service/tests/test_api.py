import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_notify_endpoint():
    response = client.post("/notify", json={
        "message": "Test Notification"
    })
    assert response.status_code == 200
