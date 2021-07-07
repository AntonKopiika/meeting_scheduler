import http
import json

import src

client = src.app.test_client()
meeting_id = 0


def test_get_meetings_with_db():
    response = client.get("/meeting")
    assert response.status_code == http.HTTPStatus.OK


def test_post_meeting_with_db():
    data = {"host": 5, "participants": [6], "meeting_start_time": "2021-07-07T12:10:44.126104",
            "meeting_end_time": "2021-07-07T12:10:44.126104",
            "host_id": 5, "title": "title", "details": "teems", "comment": "comment",
            "link": "link"}
    response = client.post("/meeting", content_type="application/json", data=json.dumps(data))
    assert response.status_code == http.HTTPStatus.CREATED
    assert response.json["title"] == "title"
    global meeting_id
    meeting_id = response.json["id"]


def test_post_wrong_data_meeting_with_db():
    data = {'name': 'username'}
    response = client.post("/meeting", content_type="application/json", data=json.dumps(data))
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_get_non_existent_meeting_with_db():
    response = client.get(f"/meeting/0")
    assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_get_meeting_by_id_with_db():
    response = client.get(f"/meeting/{meeting_id}")
    assert response.status_code == http.HTTPStatus.OK
    assert response.json["title"] == "title"


def test_put_meeting_with_db():
    data = {"host": 5, "participants": [4,6], "meeting_start_time": "2021-07-07T12:10:44.126104",
            "meeting_end_time": "2021-07-07T12:10:44.126104",
            "host_id": 5, "title": "another title", "details": "teems", "comment": "comment",
            "link": "link"}
    response = client.put(f"/meeting/{meeting_id}", content_type="application/json", data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.OK
    assert response.json["title"] == "another title"


def test_put_wrong_meeting_with_db():
    data = {'username': 'somename', 'password': 'password'}
    response = client.put(f"/meeting/{meeting_id}", content_type="application/json", data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_delete_meeting_with_db():
    response = client.delete(f"/meeting/{meeting_id}")
    assert response.status_code == http.HTTPStatus.NO_CONTENT


def test_delete_non_existent_meeting_with_db():
    response = client.delete(f"/meeting/{meeting_id}")
    assert response.status_code == http.HTTPStatus.NOT_FOUND
