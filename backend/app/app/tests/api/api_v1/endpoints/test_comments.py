from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.security import create_access_token
from app.models import Comment
from app.tests.utils import (
    comments_path,
    get_comment,
    get_comment_json,
    get_post,
    get_profile,
    get_random_string,
    get_user,
)


def test_create_comment(session: Session, client: TestClient):
    user = get_user()
    profile = get_profile(user)
    session.add(profile)
    session.commit()
    access_token = create_access_token(user.username)
    headers = {"Authorization": f"Bearer {access_token}"}
    post = get_post(profile.id or 0)
    session.add(post)
    session.commit()
    json = get_comment_json(profile.id or 0, post.id or 0)
    response = client.post(comments_path, json=json, headers=headers)
    data = response.json()
    assert response.status_code == 201
    assert data["content"] == json["content"]
    assert data["profile_id"] == json["profile_id"]
    assert data["post_id"] == json["post_id"]
    assert data["id"] == 1


def test_read_comment(session: Session, client: TestClient):
    profile_id = 1
    post_id = 1
    comment = get_comment(profile_id, post_id)
    session.add(comment)
    session.commit()
    response = client.get(f"{comments_path}/{comment.id}")
    data = response.json()
    assert response.status_code == 200
    assert data["content"] == comment.content
    assert data["profile_id"] == comment.profile_id
    assert data["post_id"] == comment.post_id
    assert data["id"] == comment.id


def test_read_comments(session: Session, client: TestClient):
    profile_id = 1
    post_id = 1
    comment1 = get_comment(profile_id, post_id)
    comment2 = get_comment(profile_id, post_id)
    session.add_all((comment1, comment2))
    session.commit()
    response = client.get(comments_path)
    data = response.json()
    assert response.status_code == 200
    assert data[0]["content"] == comment1.content
    assert data[0]["profile_id"] == comment1.profile_id
    assert data[0]["post_id"] == comment1.post_id
    assert data[0]["id"] == comment1.id
    assert data[1]["content"] == comment2.content
    assert data[1]["profile_id"] == comment2.profile_id
    assert data[1]["post_id"] == comment2.post_id
    assert data[1]["id"] == comment2.id


def test_update_comment(session: Session, client: TestClient):
    user = get_user()
    profile = get_profile(user)
    session.add(profile)
    session.commit()
    access_token = create_access_token(user.username)
    headers = {"Authorization": f"Bearer {access_token}"}
    post = get_post(profile.id or 0)
    session.add(post)
    session.commit()
    comment = get_comment(profile.id or 0, post.id or 0)
    session.add(comment)
    session.commit()
    new_data = {"content": get_random_string(5)}
    response = client.put(
        f"{comments_path}/{comment.id}", json=new_data, headers=headers
    )
    data = response.json()
    assert response.status_code == 200
    assert data["content"] == new_data["content"]
    assert data["profile_id"] == comment.profile_id
    assert data["post_id"] == comment.post_id
    assert data["id"] == comment.id


def test_delete_comment(session: Session, client: TestClient):
    user = get_user()
    profile = get_profile(user)
    session.add(profile)
    session.commit()
    access_token = create_access_token(user.username)
    headers = {"Authorization": f"Bearer {access_token}"}
    post = get_post(profile.id or 0)
    session.add(post)
    session.commit()
    comment = get_comment(profile.id or 0, post.id or 0)
    session.add(comment)
    session.commit()
    response = client.delete(f"{comments_path}/{comment.id}", headers=headers)
    data = response.json()
    db_comment = session.get(Comment, comment.id)
    assert response.status_code == 200
    assert data == {"msg": "ok"}
    assert db_comment is None
