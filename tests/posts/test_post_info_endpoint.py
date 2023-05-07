"""Testing PostInfo endpoint."""

import jwt

from src.config import Config


def test_get_post_info_endpoint_with_authorized_user_returns_200_with_correct_body(client,
                                                                                   db_with_one_of_user_topic_post):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("/api/posts/1", headers={"Authorization": f"Bearer {authorization_token}"})

    assert result.status_code == 200
    assert result.json == {
        "id": 1,
        "author_id": 1,
        "created_at": "2023-05-06 00:12:38.078953",
        "body": "test body",
        "topic_id": 1,
    }


def test_get_post_info_endpoint_with_nonexistent_post_returns_404_with_correct_body(client, db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("/api/posts/1", headers={"Authorization": f"Bearer {authorization_token}"})

    assert result.status_code == 404
    assert result.json == {"message": "Could not find a post with id provided."}
