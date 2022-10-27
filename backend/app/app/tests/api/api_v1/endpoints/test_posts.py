from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.security import create_access_token
from app.models import Post
from app.tests.utils import get_post, get_post_json, get_user, posts_path, get_profile


def test_create_post(session: Session, client: TestClient):
    user = get_user()
    profile = get_profile(user)
    session.add(profile)
    session.commit()
    access_token = create_access_token(user.username)
    headers = {"Authorization": f"Bearer {access_token}"}
    json = get_post_json(profile.id or 0)
    response = client.post(posts_path, json=json, headers=headers)
    data = response.json()
    assert response.status_code == 201
    assert data["id"] == 1
    assert data["title"] == json["title"]
    assert data["summary"] == json["summary"]
    assert data["content"] == json["content"]
    assert data["profile_id"] == profile.id


def test_read_post(session: Session, client: TestClient):
    profile_id = 1
    post = get_post(profile_id)
    session.add(post)
    session.commit()
    response = client.get(f"{posts_path}/{post.id}")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == post.id
    assert data["title"] == post.title
    assert data["summary"] == post.summary
    assert data["content"] == post.content
    assert data["profile_id"] == profile_id


def test_read_posts(session: Session, client: TestClient):
    profile_id1 = 1
    profile_id2 = 2
    post1 = get_post(profile_id1)
    post2 = get_post(profile_id2)
    session.add_all((post1, post2))
    session.commit()
    response = client.get(posts_path)
    data = response.json()
    assert response.status_code == 200
    assert data[0]["id"] == post1.id
    assert data[0]["title"] == post1.title
    assert data[0]["summary"] == post1.summary
    assert data[0]["content"] == post1.content
    assert data[0]["profile_id"] == post1.profile_id
    assert data[1]["id"] == post2.id
    assert data[1]["title"] == post2.title
    assert data[1]["summary"] == post2.summary
    assert data[1]["content"] == post2.content
    assert data[1]["profile_id"] == post2.profile_id


def test_update_post(session: Session, client: TestClient):
    user = get_user()
    profile = get_profile(user)
    session.add(profile)
    session.commit()
    access_token = create_access_token(user.username)
    headers = {"Authorization": f"Bearer {access_token}"}
    post = get_post(profile.id or 0)
    session.add(post)
    session.commit()
    new_data = get_post_json(profile.id or 0)
    del new_data["profile_id"]
    response = client.put(f"{posts_path}/{post.id}", json=new_data, headers=headers)
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == post.title
    assert data["summary"] == post.summary
    assert data["content"] == post.content
    assert data["profile_id"] == post.profile_id


def test_delete_post(session: Session, client: TestClient):
    user = get_user()
    profile = get_profile(user)
    session.add(profile)
    session.commit()
    access_token = create_access_token(user.username)
    headers = {"Authorization": f"Bearer {access_token}"}
    post = get_post(profile.id or 0)
    session.add(post)
    session.commit()
    response = client.delete(f"{posts_path}/{post.id}", headers=headers)
    data = response.json()
    db_post = session.get(Post, post.id)
    assert response.status_code == 200
    assert data == {"msg": "ok"}
    assert db_post is None
