from meeting_scheduler.src import app_factory
from meeting_scheduler.src.rest.resources import MeetingApi, Smoke, TimeslotApi, UserApi

api = app_factory.get_api()

api.add_resource(
    Smoke,
    "/smoke"
)
api.add_resource(
    UserApi,
    "/user",
    "/user/<user_id>",
    strict_slashes=False
)
api.add_resource(
    MeetingApi,
    "/meeting",
    "/meeting/<meeting_id>",
    strict_slashes=False
)
api.add_resource(
    TimeslotApi,
    "/timeslot",
    "/timeslot/<timeslot_id>",
    strict_slashes=False
)
