from datetimerange import DateTimeRange
from google_secrets_manager_client.encryption import CryptoService

from meeting_scheduler.src.db_service import get_user_meetings, get_user_timeslots
from meeting_scheduler.src.models import UserCredential


def get_free_timeslots(req):
    timeslots = get_user_timeslots(req.user, req.start, req.end)
    meetings = get_user_meetings(req)
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


def create_user_cred(cred: str, user_id: int, provider: str, description: str = None):
    crypto_service = CryptoService()
    return UserCredential(
        cred=crypto_service.encrypt(cred),
        user_id=user_id,
        provider=provider,
        description=description
    )


def decrypt_user_cred(user_cred: UserCredential):
    crypto_service = CryptoService()
    return crypto_service.decrypt(user_cred.cred)
