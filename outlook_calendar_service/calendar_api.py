from datetime import datetime

import msal
import requests

from google_secrets_manager_client.encryption import CryptoService
from meeting_scheduler.app_config import Settings
from meeting_scheduler.src.db_service import add_internal_meeting_from_outlook
from meeting_scheduler.src.models import UserAccount

settings = Settings()


class OutlookApiService:
    def __init__(self, token):
        self.token = token

    def get_user(self):
        graph_data = requests.get(
            settings.user_endpoint,
            headers={'Authorization': 'Bearer ' + self.token['access_token']},
        ).json()
        return graph_data

    def create_event(
            self,
            title,
            description,
            start_time,
            end_time,
            timezone,
            attendee_name,
            attendee_email,
            location,
            is_online_meeting=False,
            online_meeting_provider=None
    ):
        headers = {'Authorization': 'Bearer ' + self.token['access_token'],
                   'Content-Type': 'application/json'}
        json = {
            'subject': title,
            'body': {
                'contentType': 'HTML',
                'content': description or "without description"
            },
            'start': {
                'dateTime': start_time,
                'timeZone': timezone
            },
            'end': {
                'dateTime': end_time,
                'timeZone': timezone
            },
            'location': {
                'displayName': location
            },
            'attendees': [
                {
                    'emailAddress': {
                        'address': attendee_email,
                        'name': attendee_name
                    },
                    'type': 'required'
                }
            ],
        }

        if is_online_meeting:
            json["isOnlineMeeting"] = is_online_meeting,
            json["onlineMeetingProvider"] = online_meeting_provider
        graph_data = requests.post(
            settings.event_endpoint,
            headers=headers,
            json=json
        ).json()
        return graph_data

    def get_event(self, event_id=None):
        graph_data = requests.get(
            settings.event_endpoint + event_id if event_id else settings.event_endpoint,
            headers={'Authorization': 'Bearer ' + self.token['access_token']},
        ).json()
        return graph_data

    def update_event(
            self,
            event_id,
            title,
            description,
            start_time,
            end_time,
            timezone,
            location,
            is_online_meeting=False,
            online_meeting_provider=None):
        json = {
            'subject': title,
            'body': {
                'contentType': 'HTML',
                'content': description or "without description"
            },
            'start': {
                'dateTime': start_time,
                'timeZone': timezone
            },
            'end': {
                'dateTime': end_time,
                'timeZone': timezone
            },
            'location': {
                'displayName': location
            }
        }
        if is_online_meeting:
            json["isOnlineMeeting"] = is_online_meeting,
            json["onlineMeetingProvider"] = online_meeting_provider
        graph_data = requests.patch(
            settings.event_endpoint + event_id,
            headers={'Authorization': 'Bearer ' + self.token['access_token']},
            json=json
        ).json()
        return graph_data

    def delete_event(self, event_id):
        graph_data = requests.delete(
            settings.event_endpoint + event_id,
            headers={'Authorization': 'Bearer ' + self.token['access_token']},
        ).status_code
        return graph_data


def get_outlook_token_from_user_account(acc: UserAccount):
    app = msal.ConfidentialClientApplication(
        settings.outlook_client_id, authority=settings.outlook_authority,
        client_credential=settings.outlook_client_secret
    )
    cryptoservice = CryptoService()
    result = app.acquire_token_by_refresh_token(
        refresh_token=cryptoservice.decrypt(acc.cred),
        scopes=settings.scope)
    if result and "access_token" in result:
        return result
    return None


def get_user_meetings_from_outlook_account(user_acc: UserAccount):
    token = get_outlook_token_from_user_account(user_acc)
    response_json = OutlookApiService(token).get_event()
    meetings = []
    if response_json.get("value"):
        meetings = response_json["value"]
    return meetings


def sync_meetings_with_db(user_acc_id: int):
    datetime_format = "%Y-%m-%dT%H:%M:%S"
    user_acc = UserAccount.query.get(user_acc_id)
    meetings_from_outlook = get_user_meetings_from_outlook_account(user_acc)
    meetings_from_db = user_acc.user.meetings
    start_times = [meeting.start_time for meeting in meetings_from_db]

    for outlook_meeting in meetings_from_outlook:
        start = datetime.strptime(outlook_meeting["start"]["dateTime"][:-8], datetime_format)
        if start not in start_times:
            add_internal_meeting_from_outlook(outlook_meeting, user_acc.user)
