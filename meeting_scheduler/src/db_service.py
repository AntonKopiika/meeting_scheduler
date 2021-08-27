from datetime import datetime, timedelta
from typing import List, Type, Union

from datetimerange import DateTimeRange
from flask import abort
from flask_sqlalchemy import SQLAlchemy
from google_secrets_manager_client.encryption import CryptoService

from meeting_scheduler.app_config import Settings
from meeting_scheduler.src import app_factory
from meeting_scheduler.src.models import Event, Meeting, User, UserAccount
from meeting_scheduler.src.schemas.request import Request

bcrypt = app_factory.get_bcrypt()
db = app_factory.get_db()


def get_user_meetings(request: Request):
    user = User.query.get_or_404(request.user)
    meetings = [
        meeting for meeting in user.meetings if
        datetime.fromordinal(
            request.start.toordinal()
        ) <= meeting.start_time <= datetime.fromordinal(
            request.end.toordinal()
        )
    ]
    return meetings


def get_event_free_slots(event: Event):
    current_time = datetime.now()
    date_range = DateTimeRange(event.start_date, event.end_date)
    start_time = event.start_date + timedelta(
        hours=event.start_time.hour,
        minutes=event.start_time.minute
    )
    meetings = [meeting.start_time for meeting in event.meetings]
    free_slots = []
    if current_time > start_time:
        next_day = current_time + timedelta(days=1)
        next_day = datetime(year=next_day.year, month=next_day.month, day=next_day.day)
        date_range = DateTimeRange(next_day, event.end_date)
        time_delta = current_time - start_time
        start = start_time + time_delta.days * timedelta(days=1) + (
            time_delta.seconds // (60 * event.duration) + 1
        ) * timedelta(minutes=event.duration)
        if start.time() < event.end_time:
            end = start.date + timedelta(
                hours=event.end_time.hour,
                minutes=event.end_time.minute
            )
            time_range = DateTimeRange(start, end)
            slots = [
                slot for slot in
                list(time_range.range(timedelta(minutes=event.duration)))[:-1]
                if slot not in meetings]
            free_slots.extend(slots)

    for day in date_range.range(timedelta(days=1)):
        if event.working_days and day.weekday() > 4:
            continue
        else:
            start = day + timedelta(
                hours=event.start_time.hour,
                minutes=event.start_time.minute
            )
            end = day + timedelta(
                hours=event.end_time.hour,
                minutes=event.end_time.minute
            )
            time_range = DateTimeRange(start, end)
            slots = [
                slot for slot in
                list(time_range.range(timedelta(minutes=event.duration)))[:-1]
                if slot not in meetings
            ]
            free_slots.extend(slots)
    return free_slots


def add_internal_meeting_from_outlook(meeting_json: dict, host: User):
    datetime_format = Settings().datetime_format
    meeting = Meeting(
        host_id=host.id,
        start_time=datetime.strptime(
            meeting_json["start"]["dateTime"][:-8],
            datetime_format
        ),
        end_time=datetime.strptime(
            meeting_json["end"]["dateTime"][:-8],
            datetime_format
        ),
        calendar_event_id=meeting_json["id"],
        link=meeting_json["webLink"]
    )
    attendees = meeting_json["attendees"]
    if attendees:
        meeting.attendee_name = attendees[0]["emailAddress"]["name"]
        meeting.attendee_email = attendees[0]["emailAddress"]["address"]
    db.session.add(meeting)
    db.session.commit()


def create_user_account(
        email: str,
        cred: str,
        user: User,
        provider: str,
        description: str = None
):
    crypto_service = CryptoService()
    account = UserAccount.query.filter(UserAccount.email == email).first()
    if account:
        if account.user == user:
            account.email = email
            account.user = user
            account.provider = provider
            account.description = description
            account.cred = crypto_service.encrypt(cred)
        else:
            abort(400)
    else:
        account = UserAccount(
            email=email,
            cred=crypto_service.encrypt(cred),
            user=user,
            user_id=user.id,
            provider=provider,
            description=description
        )
        db.session.add(account)
    db.session.commit()
    return account


class CRUDService:
    def __init__(
            self,
            model: Type[Union[User, Meeting, Event, UserAccount]],
            db: SQLAlchemy
    ):
        self.model = model
        self.db = db

    def add(self, instance: Union[User, Meeting, Event, UserAccount]):
        self.db.session.add(instance)
        self.db.session.commit()

    def get(self, id: int) -> Union[User, Meeting, Event, UserAccount]:
        return self.model.query.get(id)

    def get_all(self) -> List[Union[User, Meeting, Event, UserAccount]]:
        return self.model.query.all()

    def update(
            self,
            instance: Union[User, Meeting, Event, UserAccount],
            update_json: dict
    ):
        if isinstance(instance, User):
            update_json["password"] = bcrypt. \
                generate_password_hash(update_json["password"]). \
                decode("utf-8")
            self.model.query.filter_by(id=instance.id).update(update_json)
        else:
            self.model.query.filter_by(id=instance.id).update(update_json)
        self.db.session.commit()

    def delete(self, instance: Union[User, Meeting, Event, UserAccount]):
        self.db.session.delete(instance)
        self.db.session.commit()
