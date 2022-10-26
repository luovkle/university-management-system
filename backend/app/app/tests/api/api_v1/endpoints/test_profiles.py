from sqlmodel import Session
from fastapi.testclient import TestClient

from app.tests.utils import profiles_path, get_profile


def test_read_profile(session: Session, client: TestClient):
    profile = get_profile()
    session.add(profile)
    session.commit()
    response = client.get(f"{profiles_path}/{profile.id}")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == profile.id
    assert data["user_id"] == profile.user_id
    assert data["username"] == profile.username
    assert data["description"] == profile.description


def test_tead_profiles(session: Session, client: TestClient):
    profile1 = get_profile()
    profile2 = get_profile()
    profiles = (profile1, profile2)
    session.add_all(profiles)
    session.commit()
    response = client.get(f"{profiles_path}")
    data = response.json()
    assert response.status_code == 200
    assert data[0]["id"] == profile1.id
    assert data[0]["user_id"] == profile1.user_id
    assert data[0]["username"] == profile1.username
    assert data[0]["description"] == profile1.description
    assert data[1]["id"] == profile2.id
    assert data[1]["user_id"] == profile2.user_id
    assert data[1]["username"] == profile2.username
    assert data[1]["description"] == profile2.description
