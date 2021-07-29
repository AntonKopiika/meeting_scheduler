from datetime import date

from datetimerange import DateTimeRange

from meeting_scheduler.src.db_service import get_user_meetings, get_user_timeslots


def get_free_timeslots(user_id: int, start_date: date, end_date: date):
    timeslots = get_user_timeslots(user_id, start_date, end_date)
    meetings = get_user_meetings(user_id, start_date, end_date)
    meeting_slots = [DateTimeRange(
        meeting.meeting_start_time,
        meeting.meeting_end_time) for meeting in meetings]
    all_slots = [DateTimeRange(slot.start_time, slot.end_time) for slot in timeslots]
    for meeting in meeting_slots:
        free_slots = []
        for slot in all_slots:
            if meeting.is_intersection(slot):
                free_slots.extend(slot.subtract(meeting))
            else:
                free_slots.append(slot)
        all_slots = free_slots
    free_slots = [
        {
            "start": str(slot.start_datetime),
            "end": str(slot.end_datetime)
        } for slot in all_slots
    ]
    return free_slots
