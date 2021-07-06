from flask_restful import Resource
from db_service import UserService
from schemas.user import UserSchema
from schemas.meeting import MeetingSchema


class Smoke(Resource):
    def get(self):
        return {"status": "OK"}, 200


class UserApi(Resource):
    user_schema = UserSchema()

    def get(self, user_id=None):
        if user_id is None:
            users = UserService.get()
            return self.user_schema.dump(users, many=True), 200
        user = UserService.get(user_id)
        if not user:
            return "", 404
        return self.user_schema.dump(user), 200

