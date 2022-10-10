from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import User
from app.tests.utils import get_user, get_user_json, users_path


def test_create_user(client: TestClient):
    json = get_user_json()
    response = client.post(users_path, json=json)
    data = response.json()
    assert response.status_code == 201
    assert data["username"] == json["username"]
    assert data["first_name"] == json["first_name"]
    assert data["last_name"] == json["last_name"]
    assert data["email"] == json["email"]
    assert data.get("password") is None


def test_create_user_invalid(client: TestClient):
    json = get_user_json()
    del json["username"]
    response = client.post(users_path, json=json)
    assert response.status_code == 422


def test_create_user_with_duplicated_data(client: TestClient):
    json = get_user_json()
    response1 = client.post(users_path, json=json)
    response2 = client.post(users_path, json=json)
    assert response1.status_code == 201
    assert response2.status_code == 400


def test_read_user(client: TestClient, session: Session):
    user = get_user()
    session.add(user)
    session.commit()
    response = client.get(f"{users_path}/1")
    data = response.json()
    assert response.status_code == 200
    assert data["username"] == user.username
    assert data["first_name"] == user.first_name
    assert data["last_name"] == user.last_name
    assert data["email"] == user.email
    assert data.get("password") is None


def test_read_users(client: TestClient, session: Session):
    user1 = get_user()
    user2 = get_user()
    session.add_all((user1, user2))
    session.commit()
    response = client.get(users_path)
    data = response.json()
    assert data[0]["username"] == user1.username
    assert data[0]["first_name"] == user1.first_name
    assert data[0]["last_name"] == user1.last_name
    assert data[0]["email"] == user1.email
    assert data[1]["username"] == user2.username
    assert data[1]["first_name"] == user2.first_name
    assert data[1]["last_name"] == user2.last_name
    assert data[1]["email"] == user2.email


def test_update_user(session: Session, client: TestClient):
    user = get_user()
    session.add(user)
    session.commit()
    new_data = {"username": "new_username"}
    response = client.put(f"{users_path}/{user.id}", json=new_data)
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == user.id
    assert data["username"] == new_data["username"]
    assert data["first_name"] == user.first_name
    assert data["last_name"] == user.last_name
    assert data["email"] == user.email
    assert data.get("password") is None
    assert data.get("hashed_password") is None


def test_delete_user(session: Session, client: TestClient):
    user = get_user()
    session.add(user)
    session.commit()
    response = client.delete(f"{users_path}/{user.id}")
    data = response.json()
    db_user = session.get(User, user.id)
    assert response.status_code == 200
    assert data == {"msg": "ok"}
    assert db_user is None
