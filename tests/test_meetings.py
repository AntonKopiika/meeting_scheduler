import http
import json
from meeting_scheduler.src.models import Meeting


def test_get_meetings_with_db(test_client):
    response = test_client.get("/meeting")
    assert response.status_code == http.HTTPStatus.OK


def test_post_meeting_with_db(test_client, db_population):
    data = {
        "host": db_population["users"][1].id,
        "participants": [db_population["users"][2].id],
        "meeting_start_time": "2021-07-07T12:10:44.126104",
        "meeting_end_time": "2021-07-07T12:10:44.126104",
        "host_id": db_population["users"][1].id,
        "title": "title",
        "details": "teems",
        "comment": "comment",
        "link": "link"
    }
    response = test_client.post("/meeting", content_type="application/json", data=json.dumps(data))
    assert response.status_code == http.HTTPStatus.CREATED
    assert response.json["title"] == "title"


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
    assert response.json["title"] == test_meeting.title


def test_put_meeting_with_db(test_client, test_meeting, db_population, db):
    data = {
        "host": db_population["users"][1].id,
        "participants": [db_population["users"][2].id, db_population["users"][3].id],
        "meeting_start_time": "2021-07-07T12:10:44.126104",
        "meeting_end_time": "2021-07-07T12:10:44.126104",
        "host_id": db_population["users"][1].id,
        "title": "another title",
        "details": "teems",
        "comment": "comment",
        "link": "link"
    }
    response = test_client.put(f"/meeting/{test_meeting.id}", content_type="application/json", data=json.dumps(data))

    assert db.session.query(Meeting).count() == 2
    assert response.status_code == http.HTTPStatus.OK
    assert response.json["title"] == "another title"


def test_put_wrong_meeting_with_db(test_client, test_meeting):
    data = {'username': 'somename', 'password': 'password'}
    response = test_client.put(f"/meeting/{test_meeting.id}", content_type="application/json", data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_delete_meeting_with_db(test_client, test_meeting):
    response = test_client.delete(f"/meeting/{test_meeting.id}")
    assert response.status_code == http.HTTPStatus.NO_CONTENT


def test_delete_non_existent_meeting_with_db(test_client):
    response = test_client.delete(f"/meeting/0")
    assert response.status_code == http.HTTPStatus.NOT_FOUND
