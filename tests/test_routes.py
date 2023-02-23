from unittest.mock import patch

from src.models import User


def test_check_unit_tests_renders_template_correctly(client, db_empty):
    with patch("src.routes.render_template") as render_template:

        result = client.post("/check-unit-tests")

    assert result.status_code == 200
    render_template.assert_called_once_with("user_created.html")


def test_check_unit_tests_creates_user_correctly(client, db_with_one_user):
    session = db_with_one_user
    with patch("src.routes.render_template"):

        result = client.post("/check-unit-tests")

    users_query = session.query(User)
    assert len(users_query.all()) == 2
    new_user = users_query.order_by(User.id.desc()).first()
    assert isinstance(new_user.id, int) and new_user.id > 0
    assert new_user.username == "user from app"
    assert new_user.password_hash == "password"
