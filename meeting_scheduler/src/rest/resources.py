import datetime
from typing import Optional

from flask import request
from flask_restful import Resource
from google_secrets_manager_client.encryption import CryptoService
from outlook_calendar_service.calendar_api import (
    OutlookApiService,
    get_outlook_token_from_user_account,
)

from meeting_scheduler.app_config import Settings
from meeting_scheduler.src import app_factory
from meeting_scheduler.src.db_service import CRUDService, create_user_account, get_user_meetings
from meeting_scheduler.src.models import Event, Meeting, User, UserAccount
from meeting_scheduler.src.schemas.event import EventSchema
from meeting_scheduler.src.schemas.meeting import MeetingSchema
from meeting_scheduler.src.schemas.request import RequestSchema
from meeting_scheduler.src.schemas.user import UserSchema
from meeting_scheduler.src.schemas.user_account import UserAccountSchema

db = app_factory.get_db()


class Smoke(Resource):
    def get(self):
        return {"status": "OK"}, 200


class UserApi(Resource):
    user_schema = UserSchema()
    user_db_service = CRUDService(User, db)

    def get(self, user_id: Optional[int] = None):
        if user_id is None:
            users = self.user_db_service.get_all()
            return self.user_schema.dump(users, many=True), 200
        user = self.user_db_service.get(user_id)
        if not user:
            return "", 404
        return self.user_schema.dump(user), 200

    def post(self):
        user = self.user_schema.deserialize(request.json)
        if user:
            self.user_db_service.add(user)
            return self.user_schema.dump(user), 201
        return "", 400

    def put(self, user_id: int):
        user = self.user_db_service.get(user_id)
        if not user:
            return "", 404
        new_user = self.user_schema.deserialize(request.json)
        if new_user:
            update_json = {
                "username": new_user.username,
                "password": new_user.password
            }
            self.user_db_service.update(user, update_json)
            return self.user_schema.dump(user), 200
        return "", 400

    def delete(self, user_id: int):
        user = self.user_db_service.get(user_id)
        if user:
            self.user_db_service.delete(user)
            return "", 204
        return "", 404


class MeetingApi(Resource):
    meeting_schema = MeetingSchema()
    request_schema = RequestSchema()
    meeting_db_service = CRUDService(Meeting, db)
    crypto_service = CryptoService()

    def get(self, meeting_id: Optional[int] = None):
        if meeting_id is None:
            if request.args:
                req = self.request_schema.get_request(request.args)
                if req:
                    meetings = get_user_meetings(req)
                    return self.meeting_schema.dump(meetings, many=True), 200
            meetings = self.meeting_db_service.get_all()
            return self.meeting_schema.dump(meetings, many=True), 200
        meeting = self.meeting_db_service.get(meeting_id)
        if not meeting:
            return "", 404
        return self.meeting_schema.dump(meeting), 200

    def post(self):
        meeting = self.meeting_schema.deserialize(request.json)
        if meeting:
            host = meeting.host
            for account in host.accounts:
                if account.provider == "outlook":
                    token = get_outlook_token_from_user_account(account)
                    outlook_service = OutlookApiService(token)
                    datetime_format = Settings().datetime_format
                    start_time = meeting.start_time.strftime(datetime_format)
                    end_time = meeting.end_time.strftime(datetime_format)

                    calendar_response = outlook_service.create_event(
                        title=meeting.event.title,
                        description=meeting.event.description,
                        start_time=start_time,
                        end_time=end_time,
                        timezone="UTC",
                        attendee_name=meeting.attendee_name,
                        attendee_email=meeting.attendee_email,
                        location=meeting.event.event_type,
                    )
                    if calendar_response.get("id", None):
                        meeting.calendar_event_id = calendar_response["id"]
            self.meeting_db_service.add(meeting)
            return self.meeting_schema.dump(meeting), 201
        return "", 400

    def put(self, meeting_id: int):
        meeting = self.meeting_db_service.get(meeting_id)
        if not meeting:
            return "", 404
        new_meeting = self.meeting_schema.deserialize(request.json)
        if new_meeting:
            update_json = {
                "host_id": new_meeting.host.id,
                "event_id": new_meeting.event.id,
                "start_time": new_meeting.start_time,
                "end_time": new_meeting.end_time,
                "calendar_event_id": new_meeting.calendar_event_id,
                "attendee_name": new_meeting.attendee_name,
                "attendee_email": new_meeting.attendee_email,
                "link": new_meeting.link,
                "additional_info": new_meeting.additional_info
            }
            host = new_meeting.host
            for account in host.accounts:
                if account.provider == "outlook":
                    token = get_outlook_token_from_user_account(account)
                    outlook_service = OutlookApiService(token)
                    datetime_format = Settings().datetime_format
                    start_time = new_meeting.start_time.strftime(datetime_format)
                    end_time = new_meeting.end_time.strftime(datetime_format)
                    outlook_service.update_event(
                        event_id=meeting.calendar_event_id,
                        title=new_meeting.event.title,
                        description=new_meeting.event.description,
                        start_time=start_time,
                        end_time=end_time,
                        timezone="UTC",
                        location=new_meeting.event.event_type
                    )
            self.meeting_db_service.update(meeting, update_json)
            return self.meeting_schema.dump(meeting), 200
        return "", 400

    def delete(self, meeting_id: int):
        meeting = self.meeting_db_service.get(meeting_id)
        if meeting:
            host = meeting.host
            for account in host.accounts:
                if account.provider == "outlook":
                    token = get_outlook_token_from_user_account(account)
                    outlook_service = OutlookApiService(token)
                    if meeting.calendar_event_id:
                        outlook_service.delete_event(
                            event_id=meeting.calendar_event_id
                        )
            self.meeting_db_service.delete(meeting)
            return "", 204
        return "", 404


class UserAccountApi(Resource):
    account_schema = UserAccountSchema()
    account_db_service = CRUDService(UserAccount, db)

    def get(self, account_id: Optional[int] = None):
        if account_id is None:
            accounts = self.account_db_service.get_all()
            return self.account_schema.dump(accounts, many=True), 200
        account = self.account_db_service.get(account_id)
        if not account:
            return "", 404
        return self.account_schema.dump(account), 200

    def post(self):
        account = self.account_schema.deserialize(request.json)
        if account:
            create_user_account(
                account.email,
                account.cred,
                account.user,
                account.provider,
                account.description
            )
            return self.account_schema.dump(account), 201
        return "", 400

    def put(self, account_id: int):
        account = self.account_db_service.get(account_id)
        if not account:
            return "", 404
        new_account = self.account_schema.deserialize(request.json)
        if new_account:
            create_user_account(
                new_account.email,
                new_account.cred,
                new_account.user,
                new_account.provider,
                new_account.description
            )
            return "", 200
        return "", 400

    def delete(self, account_id: int):
        account = self.account_db_service.get(account_id)
        if account:
            self.account_db_service.delete(account)
            return "", 204
        return "", 404


class EventApi(Resource):
    event_schema = EventSchema()
    event_db_service = CRUDService(Event, db)

    def get(self, event_id: Optional[int] = None):
        if event_id is None:
            events = self.event_db_service.get_all()
            return self.event_schema.dump(events, many=True), 200
        event = self.event_db_service.get(event_id)
        if not event:
            return "", 404
        return self.event_schema.dump(event), 200

    def post(self):
        event = self.event_schema.deserialize(request.json)
        if event:
            self.event_db_service.add(event)
            return self.event_schema.dump(event), 201
        return "", 400

    def put(self, event_id: int):
        event = self.event_db_service.get(event_id)
        if not event:
            return "", 404
        new_event = self.event_schema.deserialize(request.json)
        if new_event:
            update_json = {
                "host_id": new_event.host.id,
                "title": new_event.title,
                "start_date": new_event.start_date,
                "end_date": new_event.end_date,
                "duration": new_event.duration,
                "working_days": new_event.working_days,
                "description": new_event.description,
                "event_type": new_event.event_type,
                "start_time": new_event.start_time,
                "end_time": new_event.end_time
            }
            self.event_db_service.update(event, update_json)
            return self.event_schema.dump(event), 200
        return "", 400

    def delete(self, event_id: int):
        event = self.event_db_service.get(event_id)
        if event:
            self.event_db_service.delete(event)
            return "", 204
        return "", 404
