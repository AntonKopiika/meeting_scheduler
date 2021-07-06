from datetime import datetime
from typing import List

from main import db
from models import User, Meeting, Timeslot


class UserService:
    @staticmethod
    def create(username: str, email: str, password: str):
        db.session.add(User(username, email, password))
        db.session.commit()

    @staticmethod
    def get(user_id: int = None):
        if user_id:
            return User.query.get(user_id)
        return User.query.all()

    @staticmethod
    def update(user_id: int, username: str, email: str, password: str):
        user = UserService.get(user_id)
        if user:
            user.username = username
            user.email = email
            user.generate_password(password)
            db.session.commit()

    @staticmethod
    def delete(user_id: int):
        user = UserService.get(user_id)
        if user:
            db.session.delete(user)


class MeetingService:
    @staticmethod
    def create(host: User, participants: List[User], meeting_start_time: datetime,
               meeting_end_time: datetime, title: str, details: str, link: str, comment: str = None):
        db.session.add(Meeting(host, participants, meeting_start_time, meeting_end_time, title, details, link, comment))
        db.session.commit()

    @staticmethod
    def get(meeting_id: int = None):
        if meeting_id:
            return Meeting.query.get(meeting_id)
        return Meeting.query.all()

    @staticmethod
    def update(meeting_id: int, host: User, participants: List[User], meeting_start_time: datetime,
               meeting_end_time: datetime, title: str, details: str, link: str, comment: str = None):
        meeting = MeetingService.get(meeting_id)
        if meeting:
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
    def delete(meeting_id: int):
        meeting = MeetingService.get(meeting_id)
        if meeting:
            db.session.delete(meeting)


class TimeslotService:
    @staticmethod
    def create(start_time: datetime, end_time: datetime, user: User):
        db.session.add(Timeslot(start_time, end_time, user))
        db.session.commit()

    @staticmethod
    def get(timeslot_id: int = None):
        if timeslot_id:
            return Timeslot.query.get(timeslot_id)
        return Timeslot.query.all()

    @staticmethod
    def update(timeslot_id: int, start_time: datetime, end_time: datetime, user: User):
        timeslot = TimeslotService.get(timeslot_id)
        if timeslot:
            timeslot.start_time = start_time
            timeslot.end_time = end_time
            timeslot.user = user
            db.session.commit()

    @staticmethod
    def delete(timeslot_id: int):
        timeslot = TimeslotService.get(timeslot_id)
        if timeslot:
            db.session.delete(timeslot_id)