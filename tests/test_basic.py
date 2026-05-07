from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home_page():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to E-commerce Backend API"
    }


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok"
    }


def test_get_products():
    response = client.get("/products/")

    assert response.status_code == 200
    assert "items" in response.json()