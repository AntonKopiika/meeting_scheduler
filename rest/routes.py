from resources import UserApi, Smoke
from main import api

api.add_resource(Smoke, "/smoke", strict_slashes=False)
api.add_resource(UserApi, "/user",  f"/user/<user_id>", strict_slashes=False)
