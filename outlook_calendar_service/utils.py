from datetime import datetime

from outlook_calendar_service.calendar_api import (
    OutlookApiService,
    get_outlook_token_from_user_account,
)

from meeting_scheduler.app_config import Settings
from meeting_scheduler.src.db_service import add_internal_meeting_from_outlook

settings = Settings()


def get_user_meetings_from_outlook_account(user_acc):
    token = get_outlook_token_from_user_account(user_acc)
    response_json = OutlookApiService(token).get_event()
    meetings = []
    if response_json.get("value"):
        meetings = response_json["value"]
    return meetings


def sync_meetings_with_db(user_acc_id: int, user_acc_model):
    datetime_format = "%Y-%m-%dT%H:%M:%S"
    user_acc = user_acc_model.query.get(user_acc_id)
    meetings_from_outlook = get_user_meetings_from_outlook_account(user_acc)
    meetings_from_db = user_acc.user.meetings
    start_times = [meeting.start_time for meeting in meetings_from_db]

    for outlook_meeting in meetings_from_outlook:
        start = datetime.strptime(outlook_meeting["start"]["dateTime"][:-8], datetime_format)
        if start not in start_times:
            add_internal_meeting_from_outlook(outlook_meeting, user_acc.user)

