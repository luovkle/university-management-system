import random
import string

from app.core.config import settings
from app.models import Comment, Post, User, Profile

users_path = f"{settings.API_V1_STR}/users"
posts_path = f"{settings.API_V1_STR}/posts"
comments_path = f"{settings.API_V1_STR}/comments"
profiles_path = f"{settings.API_V1_STR}/profiles"


def get_random_string(length: int) -> str:
    letters = string.ascii_lowercase
    r_string = "".join(random.choices(letters, k=length))
    return r_string


def get_random_email(username_length: int = 5, domain_name_length: int = 5) -> str:
    username = get_random_string(username_length)
    domain_name = get_random_string(domain_name_length)
    email = f"{username}@{domain_name}.com"
    return email


def get_user_json(
    username_length: int = 5,
    first_name_length: int = 5,
    last_name_length: int = 5,
    password_length: int = 12,
) -> dict:
    json = {
        "username": get_random_string(username_length),
        "first_name": get_random_string(first_name_length),
        "last_name": get_random_string(last_name_length),
        "email": get_random_email(),
        "password": get_random_string(password_length),
    }
    return json


def get_user() -> User:
    json = get_user_json()
    user = User(**json, hashed_password=json["password"])
    return user


def get_post_json(
    profile_id: int,
    title_length: int = 5,
    summary_length: int = 5,
    content_length: int = 5,
) -> dict:
    json = {
        "title": get_random_string(title_length),
        "summary": get_random_string(summary_length),
        "content": get_random_string(content_length),
        "profile_id": profile_id,
    }
    return json


def get_post(profile_id: int) -> Post:
    json = get_post_json(profile_id)
    post = Post(**json)
    return post


def get_comment_json(profile_id: int, post_id: int, content_length: int = 5) -> dict:
    json = {
        "profile_id": profile_id,
        "post_id": post_id,
        "content": get_random_string(content_length),
    }
    return json


def get_comment(profile_id: int, post_id: int):
    json = get_comment_json(profile_id, post_id)
    comment = Comment(**json)
    return comment


def get_profile(user: User | None = None) -> Profile:
    if not user:
        user = get_user()
    profile = Profile(username=user.username, user=user)
    return profile
