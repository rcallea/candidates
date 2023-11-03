from fastapi.testclient import TestClient
from src.application import app
from faker import Faker
fake = Faker()

client = TestClient(app)

class datos_mock():
    def __init__(self):
        self.start_date = str(fake.date_of_birth().strftime('%Y-%m-%d'))
        self.end_date = str(fake.date_of_birth().strftime('%Y-%m-%d'))
        self.title = str(fake.name())
        self.educational_institution = str(fake.company())
        self.degree = "MAESTRÍA"
        self.state = "CANCELADO"
        self.candidate_id = "1"

datos = datos_mock()
    
def test_get_education():
    response = client.get("api/candidates/educations/1")
    assert response.status_code == 200
    candidate = response.json()
    assert "data" in candidate

def test_get_nonexistent_education():
    response = client.get("api/candidates/educations/9999")
    assert response.status_code == 200