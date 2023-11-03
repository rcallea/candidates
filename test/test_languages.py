from fastapi.testclient import TestClient
from src.application import app
from faker import Faker

fake = Faker()
client = TestClient(app)

class datos_mock():
    def __init__(self):
        self.language = str(fake.name())
        self.language_level = "C2"
        self.candidate_id = "1"

datos = datos_mock()

def test_get_languages():
    response = client.get("api/candidates/languages/1")
    assert response.status_code == 200

def test_create_language():
    new_language = {
        "language":datos.language,
        "language_level": datos.language_level,
        "candidate_id": datos.candidate_id
        }

    response = client.post("api/candidates/languages", json=new_language)
    assert response.status_code == 200
    created_candidate = response.json()
    assert "data" in created_candidate
    assert created_candidate["data"]["language"] == datos.language 

def test_get_language():
    response = client.get("api/candidates/languages/1")
    assert response.status_code == 200
    language = response.json()
    assert "data" in language    

def test_get_nonexistent_language():
    response = client.get("api/candidates/languages/9999")
    assert response.status_code == 200