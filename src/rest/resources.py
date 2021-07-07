from flask_restful import Resource
from marshmallow import ValidationError

from src import db
from src.db_service import UserService
from src.schemas.user import UserSchema
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
        UserService.update(user_id, new_user.username, new_user.email, new_user.password)
        return self.user_schema.dump(user), 200

    def delete(self, user_id):
        user = UserService.get(user_id)
        if user:
            UserService.delete(user)
            return "", 204
        return "", 404
