from app import schemas
from .database import client, session

def test_root(client):
    response = client.get("/")
    assert response.json().get('message') == 'Hello !'


def test_create_user(client):
    response = client.post("/users/", json={"email":"user1@gmail.com", "password":"123456"})
    # print(response.json())
    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == "user1@gmail.com"
    # assert response.json().get("email") == "user12@gmail.com"
    assert response.status_code == 201


def test_user_login(client):
    response = client.post("/login", data={"username":"user1@gmail.com", "password":"123456"})
    assert response.status_code == 200


