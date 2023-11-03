from fastapi.testclient import TestClient
from src.application import app
from faker import Faker
from datetime import date
fake = Faker()

client = TestClient(app)

class datos_mock():
    def __init__(self):
        self.curriculum = str(fake.name())
        self.description = str(fake.paragraph())
        self.candidate_id = "1"

datos = datos_mock()

def test_get_profiles():
    response = client.get("api/candidates/profiles/1")
    assert response.status_code == 200


def test_get_nonexistent_profile():
    response = client.get("api/candidates/profiles/9999")
    assert response.status_code == 404    

def test_create_profile():
    new_profile = {
        "curriculum": datos.curriculum, 
        "description": datos.description, 
        "candidate_id": "1"

    }

    response = client.post("api/candidates/profiles/", json=new_profile)
    assert response.status_code == 200
    created_candidate = response.json()
    assert "data" in created_candidate
    assert created_candidate["data"]["curriculum"] == datos.curriculum 