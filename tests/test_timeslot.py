import http
import json

import src

client = src.app.test_client()
timeslot_id = 0


def test_get_all_timeslots_with_db():
    response = client.get("/timeslot")
    assert response.status_code == http.HTTPStatus.OK


def test_post_timeslot_with_db():
    data = {"start_time": "2021-07-07T12:04:16.721598", "end_time": "2021-07-07T12:59:11.485480", "user": 5}
    response = client.post("/timeslot", content_type="application/json", data=json.dumps(data))
    assert response.status_code == http.HTTPStatus.CREATED
    global timeslot_id
    timeslot_id = response.json["id"]


def test_post_wrong_data_timeslot_with_db():
    data = {'name': 'username'}
    response = client.post("/timeslot", content_type="application/json", data=json.dumps(data))
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_get_user_by_id_with_db():
    response = client.get(f"/timeslot/{timeslot_id}")
    assert response.status_code == http.HTTPStatus.OK


def test_get_non_existent_timeslot_with_db():
    response = client.get(f"/timeslot/0")
    assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_put_timeslot_with_db():
    data = {"start_time": "2021-07-07T12:04:16.721598", "end_time": "2021-07-07T18:59:11.485480", "user": 5}
    response = client.put(f"/timeslot/{timeslot_id}", content_type="application/json", data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.OK
    assert response.json["end_time"] == "2021-07-07T18:59:11.485480"


def test_put_wrong_timeslot_with_db():
    data = {'username': 'somename', 'password': 'password'}
    response = client.put(f"/timeslot/{timeslot_id}", content_type="application/json", data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_delete_timeslot_with_db():
    response = client.delete(f"/timeslot/{timeslot_id}")
    assert response.status_code == http.HTTPStatus.NO_CONTENT


def test_delete_non_existent_timeslot_with_db():
    response = client.delete(f"/timeslot/{timeslot_id}")
    assert response.status_code == http.HTTPStatus.NOT_FOUND
