import pytest

from meeting_scheduler.src import app_factory
from meeting_scheduler.src.models import User, Meeting, Timeslot, participants
from datetime import datetime


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
        User("testuser1", "mail1", "password1"),
        User("testuser2", "mail2", "password2"),
        User("testuser3", "mail3", "password3"),
        User("testuser4", "mail4", "password4"),
    ]

    for user in users:
        db.session.add(user)
    db.session.commit()
    users_from_db = db.session.query(User).filter(User.username.like("testuser%")).all()
    meetings = [
        Meeting(
            host_id=users_from_db[0].id,
            meeting_start_time=datetime.now(),
            meeting_end_time=datetime.now(),
            title="test title",
            comment="comment",
            link="link",
            details="details",
            participants=[users_from_db[1], users_from_db[2]]
        )
    ]

    timeslots = [
        Timeslot(start_time=datetime.now(), end_time=datetime.now(), user_id=users_from_db[0].id),
        Timeslot(start_time=datetime.now(), end_time=datetime.now(), user_id=users_from_db[1].id),
        Timeslot(start_time=datetime.now(), end_time=datetime.now(), user_id=users_from_db[2].id)
    ]
    for meeting in meetings:
        db.session.add(meeting)
    for timeslot in timeslots:
        db.session.add(timeslot)
    db.session.commit()

    timeslots_from_db = db.session.query(Timeslot).filter(Timeslot.user_id.in_([user.id for user in users])).all()
    meeting_from_db = db.session.query(Meeting).filter(Meeting.host_id == users[0].id).all()

    yield {"users": users_from_db, "timeslots": timeslots_from_db, "meeting": meeting_from_db}

    db.session.query(participants).delete()
    db.session.query(Timeslot).delete()
    db.session.query(Meeting).delete()
    db.session.query(User).delete()
    db.session.commit()


@pytest.fixture(scope="session")
def test_user(db_population):
    user = db_population["users"][0]
    print(user.id)
    return db_population["users"][0]


@pytest.fixture(scope="session")
def test_meeting(db_population):
    return db_population["meeting"][0]


@pytest.fixture(scope="session")
def test_timeslot(db_population):
    return db_population["timeslots"][0]
