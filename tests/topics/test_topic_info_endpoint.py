"""Testing TopicInfo endpoint."""

import jwt

from src.config import Config


def test_get_topic_info_endpoint_with_authorized_user_returns_200_with_correct_body(client,
                                                                                    db_with_one_user_and_one_topic):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("/api/topics/1", headers={"Authorization": f"Bearer {authorization_token}"})

    assert result.status_code == 200
    assert result.json == {
        "author_id": 1,
        "created_at": "2023-05-06 00:12:38.078953",
        "description": "test desc",
        "title": "test title",
    }


def test_get_topic_info_endpoint_with_nonexistent_topic_returns_404_with_correct_body(client, db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("/api/topics/1", headers={"Authorization": f"Bearer {authorization_token}"})

    assert result.status_code == 404
    assert result.json == {"message": "Could not find a topic with id provided."}


def test_get_topic_info_endpoint_with_invalid_token_returns_401_with_correct_body(client,
                                                                                  db_with_one_user_and_one_topic):
    result = client.get("/api/topics/1", headers={"Authorization": "Bearer IvalidToken"})

    assert result.status_code == 401
    assert result.json == {"message": "invalid token"}
