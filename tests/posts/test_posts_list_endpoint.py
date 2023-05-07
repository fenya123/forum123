"""Testing PostsList endpoint."""

from datetime import datetime

import jwt

from src.config import Config
from src.posts.models import Post


def test_get_posts_list_endpoint_with_no_args_returns_200_with_correct_body(client,
                                                                            db_with_three_users_one_topic_three_posts):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics/1/posts", headers={"Authorization": f"Bearer {authorization_token}"})

    assert result.status_code == 200
    assert result.json == [
        {
            "id": 1,
            "author_id": 1,
            "body": "test body",
            "created_at": "2023-05-06 00:12:38.078953",
            "topic_id": 1,
        },
        {
            "id": 2,
            "author_id": 2,
            "body": "test body2",
            "created_at": "2023-05-07 00:12:38.078953",
            "topic_id": 1,
        },
        {
            "id": 3,
            "author_id": 3,
            "body": "test body3",
            "created_at": "2023-05-08 00:12:38.078953",
            "topic_id": 1,
        },
    ]


def test_get_posts_list_endpoint_with_nonexistent_topic_returns_404_with_correct_body(client,
                                                                                      db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics/1/posts", headers={"Authorization": f"Bearer {authorization_token}"})

    assert result.status_code == 404
    assert result.json == {"message": "topic does not exist"}


def test_get_posts_list_endpoint_with_order_by_returns_200_with_correct_body(client,
                                                                             db_with_three_users_one_topic_three_posts):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics/1/posts", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"order_by": "created_at,desc"})

    assert result.status_code == 200
    assert result.json == [
        {
            "id": 3,
            "author_id": 3,
            "body": "test body3",
            "created_at": "2023-05-08 00:12:38.078953",
            "topic_id": 1,
        },
        {
            "id": 2,
            "author_id": 2,
            "body": "test body2",
            "created_at": "2023-05-07 00:12:38.078953",
            "topic_id": 1,
        },
        {
            "id": 1,
            "author_id": 1,
            "body": "test body",
            "created_at": "2023-05-06 00:12:38.078953",
            "topic_id": 1,
        },
    ]


def test_get_posts_list_endpoint_with_empty_order_by_returns_400_with_correct_body(client, db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics/1/posts", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"order_by": ""})

    assert result.status_code == 400
    assert result.json == {"message": "empty argument value is not allowed"}


def test_get_posts_list_endpoint_with_invalid_order_by_returns_400_with_correct_body(client, db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics/1/posts", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"order_by": "InvalidArgument"})

    assert result.status_code == 400
    assert result.json == {"message": "failed parsing parameters provided"}


def test_get_posts_list_endpoint_with_not_allowed_order_by_returns_400_with_correct_body(client, db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics/1/posts", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"order_by": "author_id,desc"})

    assert result.status_code == 400
    assert result.json == {"message": "provided value is not allowed"}


def test_get_posts_list_endpoint_with_author_id_returns_200_with_correct_body(
        client, db_with_three_users_one_topic_three_posts,
):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics/1/posts", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"author_id": [1, 3]})

    assert result.status_code == 200
    assert result.json == [
        {
            "id": 1,
            "author_id": 1,
            "body": "test body",
            "created_at": "2023-05-06 00:12:38.078953",
            "topic_id": 1,
        },
        {
            "id": 3,
            "author_id": 3,
            "body": "test body3",
            "created_at": "2023-05-08 00:12:38.078953",
            "topic_id": 1,
        },
    ]


def test_get_posts_list_endpoint_with_empty_author_id_returns_400_with_correct_body(client, db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics/1/posts", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"author_id": ""})

    assert result.status_code == 400
    assert result.json == {"message": "empty argument value is not allowed"}


def test_get_posts_list_endpoint_with_invalid_author_id_returns_400_with_correct_body(client, db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics/1/posts", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"author_id": "InvalidArgument"})

    assert result.status_code == 400
    assert result.json == {"message": "author id must be an integer"}


def test_get_posts_list_endpoint_with_created_before_returns_200_with_correct_body(
    client, db_with_three_users_one_topic_three_posts,
):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics/1/posts", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"created_before": "2023-05-07 00:12:38.078953"})

    assert result.status_code == 200
    assert result.json == [
        {
            "id": 1,
            "author_id": 1,
            "body": "test body",
            "created_at": "2023-05-06 00:12:38.078953",
            "topic_id": 1,
        },
    ]


def test_get_posts_list_endpoint_with_created_after_returns_200_with_correct_body(
    client, db_with_three_users_one_topic_three_posts,
):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics/1/posts", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"created_after": "2023-05-07 00:12:38.078953"})

    assert result.status_code == 200
    assert result.json == [
        {
            "id": 3,
            "author_id": 3,
            "body": "test body3",
            "created_at": "2023-05-08 00:12:38.078953",
            "topic_id": 1,
        },
    ]


def test_get_posts_list_endpoint_with_empty_created_before_returns_400_with_correct_body(client, db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics/1/posts", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"created_before": ""})

    assert result.status_code == 400
    assert result.json == {"message": "empty argument value is not allowed"}


def test_get_posts_list_endpoint_with_invalid_created_before_returns_400_with_correct_body(client, db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.get("api/topics/1/posts", headers={"Authorization": f"Bearer {authorization_token}"},
                        query_string={"created_before": "InvalidArgument"})

    assert result.status_code == 400
    assert result.json == {"message": "invalid datetime string"}


def test_post_posts_list_endpoint_with_valid_args_returns_200_with_correct_body(client, db_with_one_user_and_one_topic):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.post("api/topics/1/posts", headers={"Authorization": f"Bearer {authorization_token}"},
                         query_string={"body": "test"})

    assert result.status_code == 200
    response_body = result.json
    post_id = response_body.pop("id")
    assert isinstance(post_id, int)
    created_at = response_body.pop("created_at")
    assert datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S.%f") < datetime.utcnow()
    assert response_body == {
        # "id": 10000,  # noqa
        "author_id": 1,
        "body": "test",
        # "created_at": "2023-05-07 11:25:17.592851",  # noqa
        "topic_id": 1,
    }


def test_post_posts_list_endpoint_with_valid_args_creates_objects_in_db_correctly(
        client, db_with_one_user_and_one_topic,
):
    session = db_with_one_user_and_one_topic
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.post("api/topics/1/posts", headers={"Authorization": f"Bearer {authorization_token}"},
                         query_string={"body": "test"})

    posts = session.query(Post).all()
    assert len(posts) == 1
    created_post = posts[0]
    assert created_post.created_at < datetime.now()
    assert created_post.body == "test"
    assert created_post.author_id == 1
    assert isinstance(created_post.id, int)


def test_post_posts_list_endpoint_with_nonexistent_topic_returns_404_with_correct_body(client,
                                                                                       db_with_one_user):
    authorization_token = jwt.encode({"user_id": 1}, Config.SECRET_KEY, algorithm="HS256")

    result = client.post("api/topics/1/posts", headers={"Authorization": f"Bearer {authorization_token}"},
                         query_string={"body": "test"})

    assert result.status_code == 404
    assert result.json == {"message": "topic does not exist"}
