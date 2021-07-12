import pytest
from meeting_scheduler.src import create_app, create_service_container, ServiceFactory, app
from meeting_scheduler.src.models import User

# TEST_DATABASE_URI = 'sqlite:///:memory:'
#
#
# @pytest.fixture(scope='session')
# def app():
#     app = create_app()
#     app['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
#     return app
#
#
# @pytest.fixture(scope='session')
# def db(app):
#     container = create_service_container(app)
#     db = ServiceFactory(container).get_db()
#     return db


@pytest.fixture(scope="session")
def test_client():
    return app.test_client()


@pytest.fixture(scope="session")
def test_users():
    return (
        User("testuser1", "mail1", "password1"),
        User("testuser2", "mail2", "password2"),
        User("testuser3", "mail3", "password3")
    )
