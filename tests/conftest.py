from datetime import datetime

import pytest

from meeting_scheduler.src import app_factory
from meeting_scheduler.src.models import Event, Meeting, User, UserAccount


@pytest.fixture(scope='session')
def app():
    app = app_factory.get_app()
    return app


@pytest.fixture(scope='session', autouse=True)
def db():
    return app_factory.get_db()


@pytest.fixture(scope="session")
def test_client(app):
    return app.test_client()


@pytest.fixture(scope="session", autouse=True)
def db_population(db):
    users = [
        User("testuser1", "password1"),
        User("testuser2", "password2"),
        User("testuser3", "password3"),
        User("testuser4", "password4")
    ]

    db.session.add_all(users)
    db.session.commit()
    users_from_db = db.session.query(User).filter(User.username.like("testuser%")).all()
    date_format = "%Y-%m-%d"
    datetime_format = "%Y-%m-%d %H:%M:%S"

    user_accounts = [
        UserAccount(
            email="test1@gmail.com",
            cred=b'qwe8qw45we65rte4',
            provider="google",
            description="",
            user_id=users_from_db[0].id),
        UserAccount(
            email="test2@gmail.com",
            cred=b'sdf8sa07sdaw6ewq8j',
            provider="google",
            description="",
            user_id=users_from_db[1].id
        ),
        UserAccount(
            email="test3@outlook.com",
            cred=b"sdf8swq8j",
            provider="microsoft",
            description="",
            user_id=users_from_db[2].id
        )
    ]
    events = [
        Event(
            host_id=users_from_db[0].id,
            title="test_event",
            start_date=datetime.strptime("2021-07-07 00:00:00", datetime_format).date(),
            end_date=datetime.strptime("2021-09-07 00:00:00", datetime_format).date(),
            duration=30,
            working_days=True,
            description="test_event",
            event_type="online",
            start_time=datetime.strptime("2021-07-07 12:00:00", datetime_format),
            end_time=datetime.strptime("2021-07-07 16:00:00", datetime_format)
        ),
        Event(
            host_id=users_from_db[1].id,
            title="test_event",
            start_date=datetime.strptime("2021-07-07 00:00:00", datetime_format).date(),
            end_date=datetime.strptime("2021-09-07 00:00:00", datetime_format).date(),
            duration=30,
            working_days=True,
            description="test_event",
            event_type="online",
            start_time=datetime.strptime("2021-07-07 12:00:00", datetime_format),
            end_time=datetime.strptime("2021-07-07 16:00:00", datetime_format)
        ),
        Event(
            host_id=users_from_db[2].id,
            title="test_event",
            start_date=datetime.strptime("2021-07-07 00:00:00", datetime_format).date(),
            end_date=datetime.strptime("2021-09-07 00:00:00", datetime_format).date(),
            duration=30,
            working_days=True,
            description="test_event",
            event_type="online",
            start_time=datetime.strptime("2021-07-07 12:00:00", datetime_format),
            end_time=datetime.strptime("2021-07-07 16:00:00", datetime_format)
        )
    ]
    db.session.add_all(user_accounts)
    db.session.add_all(events)
    db.session.commit()
    user_accounts_from_db = db.session.query(
        UserAccount). \
        filter(
        UserAccount.
            user_id.in_([user.id for user in users_from_db])) \
        .all()
    events_from_db = db.session.query(
        Event). \
        filter(
        Event.
            host_id.in_([user.id for user in users_from_db])) \
        .all()
    meetings = [
        Meeting(
            host_id=events_from_db[0].host_id,
            event_id=events_from_db[0].id,
            start_time=datetime.strptime("2021-07-07 12:00:00", datetime_format),
            calendar_event_id="sdg12d4fsf21dgd7s",
            attendee_name="test attendee",
            attendee_email="test@email.com",
            link="link",
            additional_info="some details"
        ),
        Meeting(
            host_id=events_from_db[1].host_id,
            event_id=events_from_db[1].id,
            start_time=datetime.strptime("2021-07-07 12:00:00", datetime_format),
            calendar_event_id="sdg12d4fsf21dgd7s",
            attendee_name="test attendee",
            attendee_email="test@email.com",
            link="link",
            additional_info="some details"
        )
    ]
    db.session.add_all(meetings)
    db.session.commit()

    meeting_from_db = db.session.query(Meeting).filter((Meeting.attendee_name == "test attendee")).all()

    yield {
        "users": users_from_db,
        "events": events_from_db,
        "meetings": meeting_from_db,
        "accounts": user_accounts_from_db
    }

    db.session.query(Meeting).delete()
    db.session.query(Event).delete()
    db.session.query(UserAccount).delete()
    db.session.query(User).delete()
    db.session.commit()


@pytest.fixture(scope="session")
def test_user(db_population):
    return db_population["users"][0]


@pytest.fixture(scope="session")
def test_meeting(db_population):
    return db_population["meetings"][1]


@pytest.fixture(scope="session")
def test_event(db_population):
    return db_population["events"][0]


@pytest.fixture(scope="session")
def test_account(db_population):
    return db_population["accounts"][0]
