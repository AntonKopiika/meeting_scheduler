from flask_restful import Resource
from marshmallow import ValidationError

from src import db
from src.db_service import UserService, MeetingService
from src.schemas.user import UserSchema
from src.schemas.meeting import MeetingSchema
from flask import request


class Smoke(Resource):
    def get(self):
        return {"status": "OK"}, 200


class UserApi(Resource):
    user_schema = UserSchema()

    def get(self, user_id=None):
        if user_id is None:
            users = UserService.get_all()
            return self.user_schema.dump(users, many=True), 200
        user = UserService.get(user_id)
        if not user:
            return "", 404
        return self.user_schema.dump(user), 200

    def post(self):
        try:
            user = self.user_schema.load(request.json, session=db.session)
        except ValidationError as err:
            return {"message": str(err)}, 400
        UserService.add(user)
        return self.user_schema.dump(user), 201

    def put(self, user_id):
        user = UserService.get(user_id)
        if not user:
            return "", 404
        try:
            new_user = self.user_schema.load(request.json, session=db.session)
        except ValidationError as err:
            return {"message": str(err)}, 400
        UserService.update(user, new_user.username, new_user.email, new_user.password)
        return self.user_schema.dump(user), 200

    def delete(self, user_id):
        user = UserService.get(user_id)
        if user:
            UserService.delete(user)
            return "", 204
        return "", 404


class MeetingApi(Resource):
    meeting_schema = MeetingSchema()

    def get(self, meeting_id=None):
        if meeting_id is None:
            meetings = MeetingService.get_all()
            return self.meeting_schema.dump(meetings, many=True), 200
        meeting = MeetingService.get(meeting_id)
        if not meeting:
            return "", 404
        return self.meeting_schema.dump(meeting), 200

    def post(self):
        try:
            meeting = self.meeting_schema.load(request.json, session=db.session)
        except ValidationError as err:
            return {"message": str(err)}, 400
        MeetingService.add(meeting)
        return self.meeting_schema.dump(meeting), 201

    def put(self, meeting_id):
        meeting = MeetingService.get(meeting_id)
        if not meeting:
            return "", 404
        try:
            new_meeting = self.meeting_schema.load(request.json, session=db.session)
        except ValidationError as err:
            return {"message": str(err)}, 400
        MeetingService.update(meeting, new_meeting.host, new_meeting.participants, new_meeting.meeting_start_time,
                              new_meeting.meeting_end_time, new_meeting.title, new_meeting.details, new_meeting.link,
                              new_meeting.comment)
        return self.meeting_schema.dump(meeting), 200

    def delete(self, meeting_id):
        meeting = MeetingService.get(meeting_id)
        if meeting:
            MeetingService.delete(meeting)
            return "", 204
        return "", 404
