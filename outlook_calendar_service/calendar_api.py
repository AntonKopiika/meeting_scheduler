import requests

from outlook_calendar_service import app_config


def get_user(token):
    graph_data = requests.get(
        app_config.USER_ENDPOINT,
        headers={'Authorization': 'Bearer ' + token['access_token']},
    ).json()
    return graph_data


def create_event(
        token,
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
    headers = {'Authorization': 'Bearer ' + token['access_token'],
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
        app_config.EVENT_ENDPOINT,
        headers=headers,
        json=json
    ).json()
    return graph_data


def get_event(token, event_id=None):
    graph_data = requests.get(
        app_config.EVENT_ENDPOINT + event_id if event_id else app_config.EVENT_ENDPOINT,
        headers={'Authorization': 'Bearer ' + token['access_token']},
    ).json()
    return graph_data


def update_event(
        token,
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
        app_config.EVENT_ENDPOINT + event_id,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        json=json
    ).json()
    return graph_data


def delete_event(token, event_id):
    graph_data = requests.delete(
        app_config.EVENT_ENDPOINT + event_id,
        headers={'Authorization': 'Bearer ' + token['access_token']},
    ).status_code
    return graph_data
