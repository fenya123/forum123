"""Testing UserInfo endpoint."""


import jwt

from src.config import Config


def test_get_user_info_endpoint_with_authorized_user_returns_200_with_correct_body(client,
                                                                                   db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("/api/users/1", headers={"Authorization": f"Bearer {authorization_token}"})

    assert result.status_code == 200
    assert result.json == {
        "id": 1,
        "name": "test",
    }


def test_get_user_info_endpoint_with_nonexistent_topic_returns_404_with_correct_body(client, db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("/api/users/2", headers={"Authorization": f"Bearer {authorization_token}"})

    assert result.status_code == 404
    assert result.json == {"message": "Could not find a user with id provided."}
