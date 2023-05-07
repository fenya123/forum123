"""Testing TopicList endpoint."""

from datetime import datetime

import jwt

from src.config import Config
from src.topics.models import Topic


def test_get_topic_list_endpoint_with_no_args_returns_200_with_correct_body(client,
                                                                            db_with_three_users_and_three_topics):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics", headers={"Authorization": f"Bearer {authorization_token}"})

    assert result.status_code == 200
    assert result.json == [
        {
            "id": 1,
            "author_id": 1,
            "created_at": "2023-05-06 00:12:38.078953",
            "description": "test desc",
            "title": "test title",
        },
        {
            "id": 2,
            "author_id": 2,
            "created_at": "2023-05-06 00:12:38.078953",
            "description": "test desc2",
            "title": "test title2",
        },
        {
            "id": 3,
            "author_id": 3,
            "created_at": "2023-05-07 00:12:38.078953",
            "description": "test desc3",
            "title": "test title3",
        },
    ]


def test_get_topic_list_endpoint_with_order_by_returns_200_with_correct_body(client,
                                                                             db_with_three_users_and_three_topics):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"order_by": "title,desc"})

    assert result.status_code == 200
    assert result.json == [
        {
            "id": 3,
            "author_id": 3,
            "created_at": "2023-05-07 00:12:38.078953",
            "description": "test desc3",
            "title": "test title3",
        },
        {
            "id": 2,
            "author_id": 2,
            "created_at": "2023-05-06 00:12:38.078953",
            "description": "test desc2",
            "title": "test title2",
        },
        {
            "id": 1,
            "author_id": 1,
            "created_at": "2023-05-06 00:12:38.078953",
            "description": "test desc",
            "title": "test title",
        },
    ]


def test_get_topic_list_endpoint_with_empty_order_by_returns_400_with_correct_body(client, db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"order_by": ""})

    assert result.status_code == 400
    assert result.json == {"message": "empty argument value is not allowed"}


def test_get_topic_list_endpoint_with_invalid_order_by_returns_400_with_correct_body(client, db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"order_by": "InvalidArgument"})

    assert result.status_code == 400
    assert result.json == {"message": "failed parsing parameters provided"}


def test_get_topic_list_endpoint_with_not_allowed_order_by_returns_400_with_correct_body(client, db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"order_by": "author_id,desc"})

    assert result.status_code == 400
    assert result.json == {"message": "provided value is not allowed"}


def test_get_topic_list_endpoint_with_author_id_returns_200_with_correct_body(client,
                                                                              db_with_three_users_and_three_topics):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"author_id": [1, 3]})

    assert result.status_code == 200
    assert result.json == [
        {
            "id": 1,
            "author_id": 1,
            "created_at": "2023-05-06 00:12:38.078953",
            "description": "test desc",
            "title": "test title",
        },
        {
            "id": 3,
            "author_id": 3,
            "created_at": "2023-05-07 00:12:38.078953",
            "description": "test desc3",
            "title": "test title3",
        },
    ]


def test_get_topic_list_endpoint_with_empty_author_id_returns_400_with_correct_body(client, db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"author_id": ""})

    assert result.status_code == 400
    assert result.json == {"message": "empty argument value is not allowed"}


def test_get_topic_list_endpoint_with_invalid_author_id_returns_400_with_correct_body(client, db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"author_id": "InvalidArgument"})

    assert result.status_code == 400
    assert result.json == {"message": "author id must be an integer"}


def test_get_topic_list_endpoint_with_created_before_returns_200_with_correct_body(
    client, db_with_three_users_and_three_topics,
):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"created_before": "2023-05-07 00:12:38.078953"})

    assert result.status_code == 200
    assert result.json == [
        {
            "id": 1,
            "author_id": 1,
            "created_at": "2023-05-06 00:12:38.078953",
            "description": "test desc",
            "title": "test title",
        },
        {
            "id": 2,
            "author_id": 2,
            "created_at": "2023-05-06 00:12:38.078953",
            "description": "test desc2",
            "title": "test title2",
        },
    ]


def test_get_topic_list_endpoint_with_created_after_returns_200_with_correct_body(
    client, db_with_three_users_and_three_topics,
):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"created_after": "2023-05-06 00:12:38.078953"})

    assert result.status_code == 200
    assert result.json == [
        {
            "id": 3,
            "author_id": 3,
            "created_at": "2023-05-07 00:12:38.078953",
            "description": "test desc3",
            "title": "test title3",
        },
    ]


def test_get_topic_list_endpoint_with_empty_created_before_returns_400_with_correct_body(client, db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"created_before": ""})

    assert result.status_code == 400
    assert result.json == {"message": "empty argument value is not allowed"}


def test_get_topic_list_endpoint_with_invalid_created_before_returns_400_with_correct_body(client, db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"created_before": "InvalidArgument"})

    assert result.status_code == 400
    assert result.json == {"message": "invalid datetime string"}


def test_post_topic_list_endpoint_with_valid_args_returns_200_with_correct_body(client, db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.post("api/topics", headers={"Authorization": f"Bearer {authorization_token}"},
                         query_string={"title": "test", "description": "testtest"})

    assert result.status_code == 200
    response_body = result.json
    post_id = response_body.pop("id")
    assert isinstance(post_id, int)
    assert response_body == {
        # "id": 10000,  # noqa
        "author_id": 1,
        "description": "testtest",
        "title": "test",
    }


def test_post_topic_list_endpoint_with_valid_args_creates_objects_in_db_correctly(client, db_with_one_user):
    session = db_with_one_user
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.post("api/topics", headers={"Authorization": f"Bearer {authorization_token}"},
                         query_string={"title": "test", "description": "testtest"})

    topics = session.query(Topic).all()
    assert len(topics) == 1
    created_topic = topics[0]
    assert created_topic.created_at < datetime.now()
    assert created_topic.title == "test"
    assert created_topic.description == "testtest"
    assert created_topic.author_id == 1
    assert isinstance(created_topic.id, int)


def test_post_topic_list_endpoint_with_empty_args_returns_400_with_correct_body(client, db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.post("api/topics", headers={"Authorization": f"Bearer {authorization_token}"},
                         query_string={"title": "", "description": ""})

    assert result.status_code == 400
    assert result.json == {"message": "invalid request"}


def test_get_topic_list_endpoint_with_no_bearer_prefix_returns_401_with_correct_body(client, db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics", headers={"Authorization": f"InvalidBearerPrefix {authorization_token}"})

    assert result.status_code == 401
    assert result.json == {"message": "invalid token"}


def test_get_topic_list_endpoint_with_empty_auth_token_returns_401_with_correct_body(client, db_with_one_user):

    result = client.get("api/topics", headers={"Authorization": "Bearer"})

    assert result.status_code == 401
    assert result.json == {"message": "invalid token"}


def test_get_topic_list_endpoint_with_nonexistent_user_auth_returns_401_with_correct_body(client, db_with_one_user):
    authorization_token = jwt.encode({"user_id": 0}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics", headers={"Authorization": f"Bearer {authorization_token}"})

    assert result.status_code == 403
    assert result.json == {"message": "user not found"}
