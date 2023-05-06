import datetime
import hashlib

import pytest
from alembic.config import main as alembic
from sqlalchemy.orm import scoped_session, sessionmaker

from src.app import app
from src.database import engine, session_var
from src.posts.models import Post
from src.topics.models import Topic
from src.users.models import User
from tests.utils.database import set_autoincrement_counters


def pytest_sessionstart(session):
    alembic(["upgrade", "head"])
    set_autoincrement_counters()


@pytest.fixture
def client():
    with app.test_client() as client, app.app_context():
        return client


@pytest.fixture
def db_empty():
    connection = engine.connect()
    transaction = connection.begin()
    session = scoped_session(sessionmaker(bind=connection))
    session_var.set(session)
    yield session
    transaction.rollback()
    session.remove()
    connection.close()


@pytest.fixture
def db_with_one_user(db_empty):
    session = db_empty
    user = User(id=1, username="test")
    user.password_hash = hashlib.sha256("testtest".encode()).hexdigest()
    session.add(user)
    session.commit()
    return session


@pytest.fixture
def db_with_one_user_and_one_topic(db_with_one_user):
    session = db_with_one_user
    creation_time = "2023-05-06 00:12:38.078953"
    topic = Topic(id=1, title="test title", description="test desc", author_id=1,
                  created_at=datetime.datetime.strptime(creation_time, "%Y-%m-%d %H:%M:%S.%f"))
    session.add(topic)
    session.commit()
    return session


@pytest.fixture
def db_with_three_users(db_with_one_user):
    session = db_with_one_user

    user_two = User(id=2, username="test2")
    user_two.password_hash = hashlib.sha256("testtest2".encode()).hexdigest()
    session.add(user_two)

    user_three = User(id=3, username="test3")
    user_three.password_hash = hashlib.sha256("testtest3".encode()).hexdigest()
    session.add(user_three)

    session.commit()
    return session


@pytest.fixture
def db_with_three_users_and_three_topics(db_with_three_users):
    session = db_with_three_users
    creation_time = "2023-05-06 00:12:38.078953"
    topic_one = Topic(id=1, title="test title", description="test desc", author_id=1,
                      created_at=datetime.datetime.strptime(creation_time, "%Y-%m-%d %H:%M:%S.%f"))
    session.add(topic_one)

    topic_two = Topic(id=2, title="test title2", description="test desc2", author_id=2,
                      created_at=datetime.datetime.strptime(creation_time, "%Y-%m-%d %H:%M:%S.%f"))
    session.add(topic_two)

    topic_three = Topic(id=3, title="test title3", description="test desc3", author_id=3)
    topic_three.created_at = datetime.datetime.strptime(creation_time,
                                                        "%Y-%m-%d %H:%M:%S.%f") + datetime.timedelta(days=1)
    session.add(topic_three)

    session.commit()
    return session


@pytest.fixture
def db_with_one_of_user_topic_post(db_with_one_user_and_one_topic):
    session = db_with_one_user_and_one_topic
    creation_time = "2023-05-06 00:12:38.078953"

    post = Post(id=1, author_id=1, body="test body", topic_id=1,
                created_at=datetime.datetime.strptime(creation_time, "%Y-%m-%d %H:%M:%S.%f"))

    session.add(post)
    session.commit()

    return session


@pytest.fixture
def db_with_three_users_one_topic_three_posts(db_with_three_users):
    session = db_with_three_users
    creation_time = "2023-05-06 00:12:38.078953"

    topic = Topic(id=1, title="test title", description="test desc", author_id=1,
                  created_at=datetime.datetime.strptime(creation_time, "%Y-%m-%d %H:%M:%S.%f"))
    session.add(topic)

    post_one = Post(id=1, author_id=1, body="test body", topic_id=1,
                    created_at=datetime.datetime.strptime(creation_time, "%Y-%m-%d %H:%M:%S.%f"))
    session.add(post_one)

    post_two = Post(id=2, author_id=2, body="test body2", topic_id=1)
    post_two.created_at = datetime.datetime.strptime(creation_time,
                                                     "%Y-%m-%d %H:%M:%S.%f") + datetime.timedelta(days=1)
    session.add(post_two)

    post_three = Post(id=3, author_id=3, body="test body3", topic_id=1)
    post_three.created_at = datetime.datetime.strptime(creation_time,
                                                       "%Y-%m-%d %H:%M:%S.%f") + datetime.timedelta(days=2)
    session.add(post_three)
    session.commit()

    return session
