import http
import json
from dataclasses import dataclass
from unittest.mock import patch

from meeting_scheduler.src.db_service import CRUDService

meeting_id = 0


@dataclass
class TestMeeting:
    host = 5,
    participants = [6],
    meeting_start_time = "2021-07-07T12:10:44.126104",
    meeting_end_time = "2021-07-07T12:10:44.126104",
    host_id = 5,
    title = "title",
    details = "teems",
    comment = "comment",
    link = "link"


def test_get_meetings_with_db(test_client):
    response = test_client.get("/meeting")
    assert response.status_code == http.HTTPStatus.OK


def test_get_meetings_mock_db(test_client):
    with patch.object(CRUDService, "get_all", return_value=[]) as mock_get_meeting:
        response = test_client.get("/meeting")
        mock_get_meeting.assert_called_once()
        assert response.json == []


def test_post_meeting_with_db(test_client):
    data = {
        "host": 5,
        "participants": [6],
        "meeting_start_time": "2021-07-07T12:10:44.126104",
        "meeting_end_time": "2021-07-07T12:10:44.126104",
        "host_id": 5,
        "title": "title",
        "details": "teems",
        "comment": "comment",
        "link": "link"
    }
    response = test_client.post("/meeting", content_type="application/json", data=json.dumps(data))
    assert response.status_code == http.HTTPStatus.CREATED
    assert response.json["title"] == "title"
    global meeting_id
    meeting_id = response.json["id"]


def test_post_meeting_mock_db(test_client):
    with patch.object(CRUDService, "add") as mock_add_meeting:
        data = {
            "host": 5,
            "participants": [6],
            "meeting_start_time": "2021-07-07T12:10:44.126104",
            "meeting_end_time": "2021-07-07T12:10:44.126104",
            "host_id": 5,
            "title": "title",
            "details": "teems",
            "comment": "comment",
            "link": "link"
        }
        response = test_client.post("/meeting", content_type="application/json", data=json.dumps(data))
        mock_add_meeting.assert_called_once()


def test_post_wrong_data_meeting_with_db(test_client):
    data = {'name': 'username'}
    response = test_client.post("/meeting", content_type="application/json", data=json.dumps(data))
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_get_non_existent_meeting_with_db(test_client):
    response = test_client.get(f"/meeting/0")
    assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_get_meeting_by_id_with_db(test_client):
    response = test_client.get(f"/meeting/{meeting_id}")
    assert response.status_code == http.HTTPStatus.OK
    assert response.json["title"] == "title"


def test_get_meeting_mock_db(test_client):
    with patch.object(CRUDService, "get", return_value=TestMeeting()) as mock_get_meeting:
        response = test_client.get(f"/meeting/{meeting_id}")
        mock_get_meeting.assert_called_once()


def test_put_meeting_with_db(test_client):
    data = {
        "host": 5,
        "participants": [4, 6],
        "meeting_start_time": "2021-07-07T12:10:44.126104",
        "meeting_end_time": "2021-07-07T12:10:44.126104",
        "host_id": 5,
        "title": "another title",
        "details": "teems",
        "comment": "comment",
        "link": "link"
    }
    response = test_client.put(f"/meeting/{meeting_id}", content_type="application/json", data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.OK
    assert response.json["title"] == "another title"


def test_put_meeting_mock_db(test_client):
    with patch.object(CRUDService, "get", return_value=TestMeeting()) as mock_get_meeting, \
            patch.object(CRUDService, "update") as mock_put_meeting:
        data = {
            "host": 5,
            "participants": [4, 6],
            "meeting_start_time": "2021-07-07T12:10:44.126104",
            "meeting_end_time": "2021-07-07T12:10:44.126104",
            "host_id": 5,
            "title": "another title",
            "details": "teems",
            "comment": "comment",
            "link": "link"
        }
        response = test_client.put(f"/meeting/{meeting_id}", content_type="application/json", data=json.dumps(data))
        mock_get_meeting.assert_called_once()
        mock_put_meeting.assert_called_once()


def test_put_wrong_meeting_with_db(test_client):
    data = {'username': 'somename', 'password': 'password'}
    response = test_client.put(f"/meeting/{meeting_id}", content_type="application/json", data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_delete_meeting_with_db(test_client):
    response = test_client.delete(f"/meeting/{meeting_id}")
    assert response.status_code == http.HTTPStatus.NO_CONTENT


def test_delete_meeting_mock_db(test_client):
    with patch.object(CRUDService, "get", return_value=TestMeeting()) as mock_get_meeting, \
            patch.object(CRUDService, "delete") as mock_delete_meeting:
        response = test_client.delete(f"/meeting/{meeting_id}")
        mock_get_meeting.assert_called_once()
        mock_delete_meeting.assert_called_once()


def test_delete_non_existent_meeting_with_db(test_client):
    response = test_client.delete(f"/meeting/{meeting_id}")
    assert response.status_code == http.HTTPStatus.NOT_FOUND
