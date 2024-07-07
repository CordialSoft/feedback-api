from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_login():
    response = client.post("/auth/login", json={"login": "admin", "password": "admin"})
    assert response.status_code == 200


def test_create_user():
    response = client.post("/auth/login", json={"login": "admin", "password": "admin"})
    assert response.status_code == 200
    token = response.json()["result"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/user",
        json={
            "name": "Davron",
            "surname": "Xamdamov",
            "login": "davron",
            "password": "davron",
            "role": "admin",
        },
        headers=headers,
    )
    assert response.status_code == 201
    assert response.json() == {"message": "created"}
