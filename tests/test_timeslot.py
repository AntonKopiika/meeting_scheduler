import http
import json

from meeting_scheduler.src.models import Timeslot


def test_get_all_timeslots_with_db(test_client):
    response = test_client.get("/timeslot")
    assert response.status_code == http.HTTPStatus.OK


def test_post_timeslot_with_db(test_client, test_user):
    data = {"start_time": "2021-07-07T15:04:16.721598", "end_time": "2021-07-07T16:59:11.485480", "user": test_user.id}
    response = test_client.post("/timeslot", content_type="application/json", data=json.dumps(data))
    assert response.status_code == http.HTTPStatus.CREATED
    assert Timeslot.query.count() == 4


def test_post_wrong_data_timeslot_with_db(test_client):
    data = {'name': 'username'}
    response = test_client.post("/timeslot", content_type="application/json", data=json.dumps(data))
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_get_user_by_id_with_db(test_client, test_timeslot):
    response = test_client.get(f"/timeslot/{test_timeslot.id}")
    assert response.status_code == http.HTTPStatus.OK


def test_get_non_existent_timeslot_with_db(test_client):
    response = test_client.get(f"/timeslot/0")
    assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_put_timeslot_with_db(test_client, test_timeslot, test_user, db):
    data = {"start_time": "2021-07-07T12:04:16.721598", "end_time": "2021-07-07T13:59:11.485480", "user": test_user.id}
    response = test_client.put(f"/timeslot/{test_timeslot.id}", content_type="application/json", data=json.dumps(data))
    assert db.session.query(Timeslot).count() == 4
    assert response.status_code == http.HTTPStatus.OK
    assert response.json["end_time"] == "2021-07-07T13:59:11.485480"


def test_check_timeslot_overlap(test_client, test_timeslot, test_user, db):
    data = {"start_time": "2021-07-07T16:04:16.721598", "end_time": "2021-07-07T17:00:11.485480", "user": test_user.id}
    response = test_client.put(f"/timeslot/{test_timeslot.id}", content_type="application/json", data=json.dumps(data))
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_put_wrong_timeslot_with_db(test_client, test_timeslot):
    data = {'username': 'somename', 'password': 'password'}
    response = test_client.put(f"/timeslot/{test_timeslot.id}", content_type="application/json", data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_delete_timeslot_with_db(test_client, test_timeslot):
    response = test_client.delete(f"/timeslot/{test_timeslot.id}")
    assert response.status_code == http.HTTPStatus.NO_CONTENT


def test_delete_non_existent_timeslot_with_db(test_client):
    response = test_client.delete(f"/timeslot/0")
    assert response.status_code == http.HTTPStatus.NOT_FOUND
