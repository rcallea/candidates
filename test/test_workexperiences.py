from fastapi.testclient import TestClient
from src.application import app
from faker import Faker
fake = Faker()

client = TestClient(app)

class datos_mock():
    def __init__(self):
        self.curriculum   = str(fake.name())
        self.description  = str(fake.paragraph())
        self.company      = str(fake.company())
        self.job_title    = str(fake.name())
        self.start_date   = str(fake.date_of_birth().strftime('%Y-%m-%d'))
        self.end_date     = str(fake.date_of_birth().strftime('%Y-%m-%d'))
        self.functions    = str(fake.text())
        self.job_type     = "JORNADA COMPLETA"
        self.is_actual    = str(1)
        self.candidate_id = "1"

datos = datos_mock()

def test_get_workexperiences():
    response = client.get("api/candidates/workexperiences/1")
    assert response.status_code == 200

def test_get_nonexistent_workexperience():
    response = client.get("api/candidates/workexperiences/9999")
    assert response.status_code == 200    

def test_create_workexperience():
    new_workexperience = {
        "company"      : datos.company,
        "job_title"    : datos.job_title,
        "start_date"   : datos.start_date,
        "end_date"     : datos.end_date,
        "functions"    : datos.functions,
        "job_type"     : datos.job_type,
        "is_actual"    : "1",
        "candidate_id" : "1"
    }

    response = client.post("api/candidates/workexperiences", json=new_workexperience)
    assert response.status_code == 200
    created_candidate = response.json()
    assert "data" in created_candidate
    assert created_candidate["data"]["company"] == datos.company