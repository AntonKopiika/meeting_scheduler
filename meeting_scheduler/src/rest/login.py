from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token)
from meeting_scheduler.src.models import User
from flask_login import login_user
parser = reqparse.RequestParser()
parser.add_argument('username', help='Username cannot be blank', required=True)
parser.add_argument('password', help='Password cannot be blank', required=True)


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        user = User.query.filter(User.username == data['username']).first()

        if not user:
            return {"error": "User not in DB. Register as a new user"}

        if user.check_password(data['password']):
            login_user(user)
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            has_accounts = True if len(user.accounts) else False

            return {
                'id': user.id,
                'username': user.username,
                'access_token': access_token,
                'refresh_token': refresh_token,
                'accounts': has_accounts
            }
        else:
            return {'error': 'Wrong credentials'}
