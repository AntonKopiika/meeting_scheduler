import http
import json
from unittest.mock import patch


def test_get_meetings_with_db(test_client):
    response = test_client.get("/meeting")
    assert response.status_code == http.HTTPStatus.OK


def test_post_meeting_with_db(test_client, test_user, db_population):
    with patch("outlook_calendar_service.calendar_api.OutlookApiService.create_event", autospec=True,
               return_value={}) as mock_create_meeting:
        data = {
            "host": db_population["events"][1].host.id,
            "event": db_population["events"][1].id,
            "start_time": "2021-07-07T14:00:00",
            "calendar_event_id": "ewr1sdg523dfl12kgj34i12ewa6s5d",
            "attendee_name": "test attendee",
            "attendee_email": "test@mail.com",
            "link": "link",
            "additional_info": "additional information"
        }
        response = test_client.post("/meeting", content_type="application/json", data=json.dumps(data))
        assert response.status_code == http.HTTPStatus.CREATED
        assert response.json["attendee_name"] == "test attendee"


def test_post_wrong_data_meeting_with_db(test_client):
    data = {'name': 'username'}
    response = test_client.post("/meeting", content_type="application/json", data=json.dumps(data))
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_get_non_existent_meeting_with_db(test_client):
    response = test_client.get(f"/meeting/0")
    assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_get_meeting_by_id_with_db(test_client, test_meeting):
    response = test_client.get(f"/meeting/{test_meeting.id}")
    assert response.status_code == http.HTTPStatus.OK
    assert response.json["attendee_name"] == test_meeting.attendee_name


def test_get_meeting_by_user_id_with_db(test_client, test_user):
    response = test_client.get(f"/meeting?user={test_user.id}&start=2021-7-1&end=2021-8-1")
    assert response.status_code == http.HTTPStatus.OK
    assert len(response.json) == 1


def test_put_meeting_with_db(test_client, test_meeting, db_population, db):
    with patch("outlook_calendar_service.calendar_api.OutlookApiService.update_event", autospec=True,
               return_value={}) as mock_put_meeting:
        data = {
            "host": db_population["events"][1].host.id,
            "event": db_population["events"][1].id,
            "start_time": "2021-07-07T14:00:00",
            "calendar_event_id": "ewr1sdg523dfl12kgj34i12ewa6s5d",
            "attendee_name": "attendee",
            "attendee_email": "test@mail.com",
            "link": "link",
            "additional_info": "additional information"
        }
        response = test_client.put(f"/meeting/{test_meeting.id}", content_type="application/json", data=json.dumps(data))
        assert response.status_code == http.HTTPStatus.OK
        assert response.json["attendee_name"] == "attendee"


def test_put_wrong_meeting_with_db(test_client, test_meeting):
    data = {'username': 'somename', 'password': 'password'}
    response = test_client.put(f"/meeting/{test_meeting.id}", content_type="application/json", data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_delete_meeting_with_db(test_client, test_meeting):
    with patch("outlook_calendar_service.calendar_api.OutlookApiService.delete_event", autospec=True,
               return_value={}) as mock_delete_meeting:
        response = test_client.delete(f"/meeting/{test_meeting.id}")
        assert response.status_code == http.HTTPStatus.NO_CONTENT


def test_delete_non_existent_meeting_with_db(test_client):
    response = test_client.delete(f"/meeting/0")
    assert response.status_code == http.HTTPStatus.NOT_FOUND
