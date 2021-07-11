from meeting_scheduler.src import ServiceFactory, container
from meeting_scheduler.src.rest.resources import Smoke, UserApi, MeetingApi, TimeslotApi

api = ServiceFactory(container).get_api()

api.add_resource(Smoke, "/smoke")
api.add_resource(UserApi, "/user", "/user/<user_id>", strict_slashes=False)
api.add_resource(MeetingApi, "/meeting", "/meeting/<meeting_id>", strict_slashes=False)
api.add_resource(TimeslotApi, "/timeslot", "/timeslot/<timeslot_id>", strict_slashes=False)
