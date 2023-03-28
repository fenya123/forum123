import pytest
from alembic.config import main as alembic
from sqlalchemy.orm import scoped_session, sessionmaker

from src import app
from src.database import engine, session_var
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
