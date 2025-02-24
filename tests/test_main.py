import pytest
from fastapi.testclient import TestClient
from app.main import app

# Create a test client
client = TestClient(app)

# Test the /orders endpoint
def test_get_orders():
    response = client.get("/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)