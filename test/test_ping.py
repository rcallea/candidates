from fastapi.testclient import TestClient
from src.application import app

client = TestClient(app)

def test_healthcheck():
    response = client.get("/api/candidates/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong", "data":"", "errors":""}