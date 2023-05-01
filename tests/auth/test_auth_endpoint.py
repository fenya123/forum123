"""Testing auth endpoint."""

import jwt

from src.config import Config


def test_post_auth_endpoint_with_nonexistent_user_returns_400_with_correct_message(client, db_empty):
    result = client.post("/api/auth", data={"username": "test", "password": "testtest"})

    assert result.status_code == 400
    assert result.json == {"message": "couldn't find user with credentials provided"}


def test_post_auth_endpoint_with_existing_user_returns_correct_body(client, db_with_one_user):
    result = client.post("/api/auth", data={"username": "test", "password": "testtest"})

    assert result.status_code == 200
    assert result.json == jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")
