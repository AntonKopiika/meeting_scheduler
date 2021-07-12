import http
import json
from dataclasses import dataclass
from unittest.mock import patch

from meeting_scheduler.src.db_service import CRUDService

timeslot_id = 0


@dataclass
class TestTimeslot:
    start_time = "2021-07-07T12:04:16.721598",
    end_time = "2021-07-07T12:59:11.485480",
    user = 5


def test_get_all_timeslots_with_db(test_client):
    response = test_client.get("/timeslot")
    assert response.status_code == http.HTTPStatus.OK


def test_get_all_timeslots_mock_db(test_client):
    with patch.object(CRUDService, "get_all", return_value=[]) as mock_get_timeslot:
        response = test_client.get("/timeslot")
        mock_get_timeslot.assert_called_once()
        assert response.json == []


def test_post_timeslot_with_db(test_client):
    data = {"start_time": "2021-07-07T12:04:16.721598", "end_time": "2021-07-07T12:59:11.485480", "user": 5}
    response = test_client.post("/timeslot", content_type="application/json", data=json.dumps(data))
    assert response.status_code == http.HTTPStatus.CREATED
    global timeslot_id
    timeslot_id = response.json["id"]


def test_post_timeslot_mock_db(test_client):
    with patch.object(CRUDService, "add") as mock_add_timeslot:
        data = {"start_time": "2021-07-07T12:04:16.721598", "end_time": "2021-07-07T12:59:11.485480", "user": 5}
        response = test_client.post("/timeslot", content_type="application/json", data=json.dumps(data))
        mock_add_timeslot.assert_called_once()


def test_post_wrong_data_timeslot_with_db(test_client):
    data = {'name': 'username'}
    response = test_client.post("/timeslot", content_type="application/json", data=json.dumps(data))
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_get_user_by_id_with_db(test_client):
    response = test_client.get(f"/timeslot/{timeslot_id}")
    assert response.status_code == http.HTTPStatus.OK


def test_get_user_mock_db(test_client):
    with patch.object(CRUDService, "get", return_value=TestTimeslot()) as mock_get_timeslot:
        response = test_client.get(f"/timeslot/{timeslot_id}")
        mock_get_timeslot.assert_called_once()


def test_get_non_existent_timeslot_with_db(test_client):
    response = test_client.get(f"/timeslot/0")
    assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_put_timeslot_with_db(test_client):
    data = {"start_time": "2021-07-07T12:04:16.721598", "end_time": "2021-07-07T18:59:11.485480", "user": 5}
    response = test_client.put(f"/timeslot/{timeslot_id}", content_type="application/json", data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.OK
    assert response.json["end_time"] == "2021-07-07T18:59:11.485480"


def test_put_timeslot_mock_db(test_client):
    with patch.object(CRUDService, "get", return_value=TestTimeslot()) as mock_get_timeslot, \
            patch.object(CRUDService, "update") as mock_put_timeslot:
        data = {"start_time": "2021-07-07T12:04:16.721598", "end_time": "2021-07-07T18:59:11.485480", "user": 5}
        response = test_client.put(f"/timeslot/{timeslot_id}", content_type="application/json", data=json.dumps(data))
        mock_get_timeslot.assert_called_once()
        mock_put_timeslot.assert_called_once()


def test_put_wrong_timeslot_with_db(test_client):
    data = {'username': 'somename', 'password': 'password'}
    response = test_client.put(f"/timeslot/{timeslot_id}", content_type="application/json", data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_delete_timeslot_with_db(test_client):
    response = test_client.delete(f"/timeslot/{timeslot_id}")
    assert response.status_code == http.HTTPStatus.NO_CONTENT


def test_delete_timeslot_mock_db(test_client):
    with patch.object(CRUDService, "get", return_value=TestTimeslot()) as mock_get_timeslot, \
            patch.object(CRUDService, "delete") as mock_delete_timeslot:
        response = test_client.delete(f"/timeslot/{timeslot_id}")
        mock_get_timeslot.assert_called_once()
        mock_delete_timeslot.assert_called_once()


def test_delete_non_existent_timeslot_with_db(test_client):
    response = test_client.delete(f"/timeslot/{timeslot_id}")
    assert response.status_code == http.HTTPStatus.NOT_FOUND
