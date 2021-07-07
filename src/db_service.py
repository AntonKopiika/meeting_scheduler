from datetime import datetime
from typing import List
from src import db
from .models import User, Meeting, Timeslot


class UserService:

    @staticmethod
    def add(user: User) -> None:
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def get(user_id: int) -> User:
        return User.query.get(user_id)

    @staticmethod
    def get_all() -> List[User]:
        return User.query.all()

    @staticmethod
    def update(user_id: User, username: str, email: str, password: str) -> None:
        db.session.query(User).filter_by(id=user_id).update(
            dict(username=username, email=email, password=password)
        )
        db.session.commit()

    @staticmethod
    def delete(user: User) -> None:
        db.session.delete(user)
        db.session.commit()


class MeetingService:

    @staticmethod
    def add(meeting: Meeting) -> None:
        db.session.add(meeting)

    @staticmethod
    def get(meeting_id: int) -> Meeting:
        return Meeting.query.get(meeting_id)

    @staticmethod
    def get_all() -> List[Meeting]:
        return Meeting.query.all()

    @staticmethod
    def update(meeting: Meeting, host: User, participants: List[User], meeting_start_time: datetime,
               meeting_end_time: datetime, title: str, details: str, link: str, comment: str = None) -> None:
        meeting.host = host
        meeting.participants = participants
        meeting.meeting_start_time = meeting_start_time
        meeting.meeting_end_time = meeting_end_time
        meeting.title = title
        meeting.details = details
        meeting.link = link
        meeting.comment = comment
        db.session.commit()

    @staticmethod
    def delete(meeting: Meeting):
        db.session.delete(meeting)


class TimeslotService:
    @staticmethod
    def add(timeslot: Timeslot) -> None:
        db.session.add(timeslot)
        db.session.commit()

    @staticmethod
    def get(timeslot_id: int) -> Timeslot:
        return Timeslot.query.get(timeslot_id)

    @staticmethod
    def get_all() -> List[Timeslot]:
        return Timeslot.query.all()

    @staticmethod
    def update(timeslot: Timeslot, start_time: datetime, end_time: datetime, user: User) -> None:
        timeslot.start_time = start_time
        timeslot.end_time = end_time
        timeslot.user = user
        db.session.commit()

    @staticmethod
    def delete(timeslot: Timeslot) -> None:
        db.session.delete(timeslot)
