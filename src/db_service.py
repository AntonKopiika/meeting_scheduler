from datetime import datetime
from typing import List
from src import db
from .models import User, Meeting, Timeslot
from werkzeug.security import generate_password_hash


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
    def update(user: User, username: str, email: str, password: str) -> None:
        db.session.query(User).filter_by(id=user.id).update(
            dict(username=username, email=email, password=generate_password_hash(password))
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
        db.session.commit()

    @staticmethod
    def get(meeting_id: int) -> Meeting:
        return Meeting.query.get(meeting_id)

    @staticmethod
    def get_all() -> List[Meeting]:
        return Meeting.query.all()

    @staticmethod
    def update(meeting: Meeting, host: User, participants: List[User], meeting_start_time: datetime,
               meeting_end_time: datetime, title: str, details: str, link: str, comment: str) -> None:
        meeting.participants = participants
        db.session.query(Meeting).filter_by(id=meeting.id).update(
            dict(host_id=host.id, meeting_start_time=meeting_start_time, meeting_end_time=meeting_end_time, title=title,
                 details=details, link=link, comment=comment)
        )

    @staticmethod
    def delete(meeting: Meeting):
        db.session.delete(meeting)
        db.session.commit()


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
        db.session.query(Timeslot).filter_by(id=timeslot.id).update(
            dict(start_time=start_time, end_time=end_time, user_id=user.id)
        )
        db.session.commit()

    @staticmethod
    def delete(timeslot: Timeslot) -> None:
        db.session.delete(timeslot)
        db.session.commit()
