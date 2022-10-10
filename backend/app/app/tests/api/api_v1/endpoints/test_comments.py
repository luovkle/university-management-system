from fastapi.testclient import TestClient
from sqlmodel import Session

from app.tests.utils import get_comment, get_comment_json, comments_path


def test_create_comment(client: TestClient):
    user_id = 1
    post_id = 1
    json = get_comment_json(user_id, post_id)
    response = client.post(comments_path, json=json)
    data = response.json()
    assert response.status_code == 201
    assert data["content"] == json["content"]
    assert data["user_id"] == json["user_id"]
    assert data["post_id"] == json["post_id"]
    assert data["id"] == 1


def test_read_comment(session: Session, client: TestClient):
    user_id = 1
    post_id = 1
    comment = get_comment(user_id, post_id)
    session.add(comment)
    session.commit()
    response = client.get(f"{comments_path}/{comment.id}")
    data = response.json()
    assert response.status_code == 200
    assert data["content"] == comment.content
    assert data["user_id"] == comment.user_id
    assert data["post_id"] == comment.post_id
    assert data["id"] == comment.id


def test_read_comments(session: Session, client: TestClient):
    user_id = 1
    post_id = 1
    comment1 = get_comment(user_id, post_id)
    comment2 = get_comment(user_id, post_id)
    session.add_all((comment1, comment2))
    session.commit()
    response = client.get(comments_path)
    data = response.json()
    assert response.status_code == 200
    assert data[0]["content"] == comment1.content
    assert data[0]["user_id"] == comment1.user_id
    assert data[0]["post_id"] == comment1.post_id
    assert data[0]["id"] == comment1.id
    assert data[1]["content"] == comment2.content
    assert data[1]["user_id"] == comment2.user_id
    assert data[1]["post_id"] == comment2.post_id
    assert data[1]["id"] == comment2.id
