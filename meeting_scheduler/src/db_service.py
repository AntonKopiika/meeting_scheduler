from datetime import date, datetime
from typing import List, Type, Union

from datetimerange import DateTimeRange
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

from meeting_scheduler.src import app_factory
from meeting_scheduler.src.models import Meeting, Timeslot, User
from meeting_scheduler.src.schemas.request import Request

bcrypt = app_factory.get_bcrypt()


def dont_have_timeslot_overlap(timeslot: Timeslot, timeslot_to_update: Timeslot = None):
    user = timeslot.user
    user_timeslots = \
        [timeslot for timeslot in user.timeslots
         if timeslot != timeslot_to_update]
    for slot in user_timeslots:
        if DateTimeRange(slot.start_time,
                         slot.end_time).is_intersection(
            DateTimeRange(timeslot.start_time,
                          timeslot.end_time)):
            return False
    return True


def dont_have_meeting_overlap(meeting: Meeting, meeting_to_update: Meeting = None):
    host = meeting.host
    host_meetings = \
        [meeting for meeting in host.meetings + host.invitations
         if meeting != meeting_to_update]
    for h_meeting in host_meetings:
        if DateTimeRange(h_meeting.meeting_start_time,
                         h_meeting.meeting_end_time).is_intersection(
            DateTimeRange(meeting.meeting_start_time,
                          meeting.meeting_end_time)):
            return False
    participants = meeting.participants
    for participant in participants:
        participant_meetings = \
            [meeting for meeting in participant.meetings + participant.invitations
             if meeting != meeting]
        for p_meeting in participant_meetings:
            if DateTimeRange(p_meeting.meeting_start_time,
                             p_meeting.meeting_end_time).is_intersection(
                DateTimeRange(meeting.meeting_start_time,
                              meeting.meeting_end_time)):
                return False
    return True


def are_participants_have_timeslot(meeting: Meeting):
    def is_user_have_free_time(user: User):
        for slot in user.timeslots:
            timeslot = DateTimeRange(slot.start_time, slot.end_time)
            if meeting.meeting_start_time in timeslot \
                    and meeting.meeting_end_time in timeslot:
                return True
        return False

    return all(map(is_user_have_free_time, meeting.participants))


def get_user_meetings(request: Request):
    user = User.query.get_or_404(request.user)
    all_meetings = user.meetings + user.invitations
    meetings = [
        meeting for meeting in all_meetings if
        datetime.fromordinal(
            request.start.toordinal()
        ) <= meeting.meeting_start_time <= datetime.fromordinal(
            request.end.toordinal()
        )
    ]
    return meetings


def get_user_timeslots(user_id: int, start_date: date, end_date: date):
    timeslots = Timeslot.query.filter(
        and_(
            Timeslot.user_id == user_id,
            Timeslot.start_time >= start_date,
            Timeslot.start_time <= end_date
        )
    ).all()
    return timeslots


class CRUDService:
    def __init__(
            self,
            model: Type[Union[User, Meeting, Timeslot]],
            db: SQLAlchemy
    ):
        self.model = model
        self.db = db

    def add(self, instance: Union[User, Meeting, Timeslot]):
        self.db.session.add(instance)
        self.db.session.commit()

    def get(self, id: int) -> Union[User, Meeting, Timeslot]:
        return self.model.query.get(id)

    def get_all(self) -> List[Union[User, Meeting, Timeslot]]:
        return self.model.query.all()

    def update(
            self,
            instance: Union[User, Meeting, Timeslot],
            update_json: dict
    ):
        if isinstance(instance, User):
            update_json["password"] = bcrypt. \
                generate_password_hash(update_json["password"]). \
                decode("utf-8")
            self.model.query.filter_by(id=instance.id).update(update_json)
        elif isinstance(instance, Meeting):
            instance.participants = update_json["participants"]
            update_json.pop("participants")
            self.model.query.filter_by(id=instance.id).update(update_json)
        elif isinstance(instance, Timeslot):
            instance.start_time = update_json["start_time"]
            instance.end_time = update_json["end_time"]
            instance.user_id = update_json["user"]
            self.db.session.add(instance)
        self.db.session.commit()

    def delete(self, instance: Union[User, Meeting, Timeslot]):
        self.db.session.delete(instance)
        self.db.session.commit()
