from src import api
from src.rest.resources import Smoke, UserApi

api.add_resource(Smoke, "/smoke")
api.add_resource(UserApi, "/user",  "/user/<user_id>", strict_slashes=False)
