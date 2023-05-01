import hashlib

import pytest
from alembic.config import main as alembic
from sqlalchemy.orm import scoped_session, sessionmaker

from src.app import app
from src.database import engine, session_var
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
