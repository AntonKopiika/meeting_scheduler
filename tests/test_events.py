import http
import json

from meeting_scheduler.src.models import Event


def test_get_all_events_with_db(test_client):
    response = test_client.get("/event")
    assert response.status_code == http.HTTPStatus.OK


def test_post_event_with_db(test_client, test_user):
    data = {
        'host': test_user.id,
        'title': "test title",
        'start_date': "2021-07-07",
        'end_date': "2021-09-07",
        'duration': 30,
        'working_days': True,
        'description': 'test description',
        'event_type': 'online meeting',
        "start_time": "2021-07-07T12:00:00",
        "end_time": "2021-07-07T17:00:00",
    }
    response = test_client.post("/event", content_type="application/json", data=json.dumps(data))
    assert response.status_code == http.HTTPStatus.CREATED


def test_post_wrong_data_event_with_db(test_client):
    data = {'name': 'username'}
    response = test_client.post("/event", content_type="application/json", data=json.dumps(data))
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_get_event_by_id_with_db(test_client, test_event):
    response = test_client.get(f"/event/{test_event.id}")
    assert response.status_code == http.HTTPStatus.OK


def test_get_non_existent_event_with_db(test_client):
    response = test_client.get(f"/event/0")
    assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_put_event_with_db(test_client, test_user, db_population, db):
    data = {
        'host': test_user.id,
        'title': "test title",
        'start_date': "2021-07-07",
        'end_date': "2021-09-07",
        'duration': 30,
        'working_days': True,
        'description': 'test description',
        'event_type': 'online meeting',
        "start_time": "2021-07-07T12:00:00",
        "end_time": "2021-07-07T17:00:00",
    }
    response = test_client.put(f"/event/{db_population['events'][1].id}", content_type="application/json", data=json.dumps(data))
    assert db.session.query(Event).count() == 4
    assert response.status_code == http.HTTPStatus.OK
    assert response.json["end_date"] == "2021-09-07"

#
# def test_check_timeslot_overlap(test_client, test_timeslot, test_user, db):
#     data = {"start_time": "2021-07-07T14:00:00", "end_time": "2021-07-07T15:00:00", "user": test_user.id}
#     response = test_client.post(f"/timeslot/", content_type="application/json", data=json.dumps(data))
#     assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_put_wrong_event_with_db(test_client, test_event):
    data = {'username': 'somename', 'password': 'password'}
    response = test_client.put(f"/event/{test_event.id}", content_type="application/json", data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_delete_event_with_db(test_client, test_event):
    response = test_client.delete(f"/event/{test_event.id}")
    assert response.status_code == http.HTTPStatus.NO_CONTENT


def test_delete_non_existent_event_with_db(test_client):
    response = test_client.delete(f"/event/0")
    assert response.status_code == http.HTTPStatus.NOT_FOUND
