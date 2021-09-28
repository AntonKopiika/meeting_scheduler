from datetime import datetime

from meeting_scheduler.app_config import Settings
from meeting_scheduler.src import app_factory
from meeting_scheduler.src.models import Event, Meeting, User, UserAccount


def populate_db():
    db = app_factory.get_db()

    users = [
        User("Reginald Wilbur", "1234"),
        User("Anton Kopiika", "1234"),
        User("Francis Alberts", "1234"),
        User("Blaze Mortimer", "1234")
    ]

    db.session.add_all(users)
    db.session.commit()
    datetime_format = Settings().datetime_format

    events = [
        Event(
            host=users[0],
            title="test_event",
            start_date=datetime.strptime("2021-09-07T00:00:00", datetime_format).date(),
            end_date=datetime.strptime("2021-10-07T00:00:00", datetime_format).date(),
            duration=30,
            working_days=True,
            description="test_event",
            event_type="online",
            start_time=datetime.strptime("2021-09-07T12:00:00", datetime_format),
            end_time=datetime.strptime("2021-10-07T16:00:00", datetime_format)
        ),
        Event(
            host=users[1],
            title="test_event",
            start_date=datetime.strptime("2021-09-07T00:00:00", datetime_format).date(),
            end_date=datetime.strptime("2021-10-07T00:00:00", datetime_format).date(),
            duration=30,
            working_days=True,
            description="test_event",
            event_type="online",
            start_time=datetime.strptime("2021-09-07T12:00:00", datetime_format),
            end_time=datetime.strptime("2021-10-07T16:00:00", datetime_format)
        ),
        Event(
            host=users[2],
            title="test_event",
            start_date=datetime.strptime("2021-09-07T00:00:00", datetime_format).date(),
            end_date=datetime.strptime("2021-10-07T00:00:00", datetime_format).date(),
            duration=30,
            working_days=True,
            description="test_event",
            event_type="online",
            start_time=datetime.strptime("2021-09-07T12:00:00", datetime_format),
            end_time=datetime.strptime("2021-10-07T16:00:00", datetime_format)
        )
    ]
    db.session.add_all(events)
    db.session.commit()
    meetings = [
        Meeting(
            host=events[0].host,
            event=events[0],
            start_time=datetime.strptime("2021-07-07T12:00:00", datetime_format),
            end_time=datetime.strptime("2021-07-07T12:30:00", datetime_format),
            calendar_event_id="sdg12d4fsf21dgd7s",
            attendee_name="test attendee",
            attendee_email="test@gmail.com",
            link="link",
            additional_info="some details"
        ),
        Meeting(
            host=events[1].host,
            event=events[1],
            start_time=datetime.strptime("2021-07-07T12:00:00", datetime_format),
            end_time=datetime.strptime("2021-07-07T12:30:00", datetime_format),
            calendar_event_id="sdg12d4fsf21dgd7s",
            attendee_name="test attendee",
            attendee_email="test@gmail.com",
            link="link",
            additional_info="some details"
        )
    ]
    db.session.add_all(meetings)
    db.session.commit()
