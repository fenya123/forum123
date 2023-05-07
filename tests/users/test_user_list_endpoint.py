"""Testing UserList endpoint."""

import jwt

from src.config import Config


def test_get_user_list_endpoint_with_no_args_returns_200_with_correct_body(client,
                                                                           db_with_three_users):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/users", headers={"Authorization": f"Bearer {authorization_token}"})

    assert result.status_code == 200
    assert result.json == [
        {
            "id": 1,
            "username": "test",
        },
        {
            "id": 2,
            "username": "test2",
        },
        {
            "id": 3,
            "username": "test3",
        },
    ]


def test_get_user_list_endpoint_with_order_by_returns_200_with_correct_body(client,
                                                                            db_with_three_users):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/users", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"order_by": "username,desc"})

    assert result.status_code == 200
    assert result.json == [
        {
            "id": 3,
            "username": "test3",
        },
        {
            "id": 2,
            "username": "test2",
        },
        {
            "id": 1,
            "username": "test",
        },
    ]


def test_get_user_list_endpoint_with_empty_order_by_returns_400_with_correct_body(client, db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/users", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"order_by": ""})

    assert result.status_code == 400
    assert result.json == {"message": "empty argument value is not allowed"}


def test_get_user_list_endpoint_with_invalid_order_by_returns_400_with_correct_body(client, db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/users", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"order_by": "InvalidArgument"})

    assert result.status_code == 400
    assert result.json == {"message": "failed parsing parameters provided"}


def test_get_user_list_endpoint_with_not_allowed_order_by_returns_400_with_correct_body(client, db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/users", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"order_by": "password_hash,desc"})

    assert result.status_code == 400
    assert result.json == {"message": "provided value is not allowed"}
