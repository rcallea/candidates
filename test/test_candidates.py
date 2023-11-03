from fastapi.testclient import TestClient
from src.application import app
from faker import Faker
from datetime import date
fake = Faker()

client = TestClient(app)

class datos_mock():
    def __init__(self):
        self.full_name = str(fake.first_name())
        self.surnames = str(fake.last_name())
        self.age = str(fake.random_int(min=18, max=60) )
        self.document_type = "CC"
        self.document = str(fake.random_int(min=10000000, max=99999999) )
        self.phone = str(fake.phone_number())
        self.birthdate = str(fake.date_of_birth().strftime('%Y-%m-%d'))
        self.country = str(fake.country())
        self.city = str(fake.city())
        self.email = str(fake.email())
        self.address = str(fake.address())
        self.soft_skills = []
        self.technical_skills = []
        self.personality_traits = []

datos = datos_mock()

def test_get_candidates():
    response = client.get("api/candidates?soft_skills=[1,2,3]&technical_skills=[4,5,6]&personality_traits=[7,8,9]")
    assert response.status_code == 200

def test_get_candidate():
    response = client.get("api/candidates/1")
    assert response.status_code == 200
    candidate = response.json()
    assert "data" in candidate
    assert candidate["data"]["id"] == 1


def test_get_nonexistent_candidate():
    response = client.get("api/candidates/9999")
    assert response.status_code == 404


def test_create_candidate():
    new_candidate = {
        "full_name":datos.full_name, 
        "surnames":datos.surnames, 
        "age":datos.age, 
        "document_type":"CC", 
        "document":datos.document, 
        "phone":datos.phone, 
        "birthdate":datos.birthdate, 
        "country":datos.country,
        "city":datos.city, 
        "email":datos.email, 
        "address":datos.address

    }

    response = client.post("api/candidates/", json=new_candidate)
    assert response.status_code == 200
    created_candidate = response.json()
    assert "data" in created_candidate
    assert created_candidate["data"]["full_name"] == datos.full_name

def test_create_candidate_exist():
    new_candidate = {
        "full_name":datos.full_name, 
        "surnames":datos.surnames, 
        "age":datos.age, 
        "document_type":"CC", 
        "document":datos.document, 
        "phone":datos.phone, 
        "birthdate":datos.birthdate, 
        "country":datos.country,
        "city":datos.city, 
        "email":datos.email, 
        "address":datos.address
    }

    response = client.post("api/candidates/", json=new_candidate)
    assert response.status_code == 210

