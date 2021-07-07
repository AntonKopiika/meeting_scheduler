import http
import json

import src

client = src.app.test_client()
user_id = 0


def test_get_users_with_db():
    response = client.get("/user")
    assert response.status_code == http.HTTPStatus.OK


def test_post_user_with_db():
    data = {'username': 'username', 'email': 'email', 'password': 'password'}
    response = client.post("/user", content_type="application/json", data=json.dumps(data))
    assert response.status_code == http.HTTPStatus.CREATED
    assert response.json["username"] == "username"
    global user_id
    user_id = response.json["id"]


def test_post_wrong_data_user_with_db():
    data = {'name': 'username'}
    response = client.post("/user", content_type="application/json", data=json.dumps(data))
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_get_user_by_id_with_db():
    response = client.get(f"/user/{user_id}")
    assert response.status_code == http.HTTPStatus.OK
    assert response.json["username"] == "username"


def test_get_non_existent_user_with_db():
    response = client.get(f"/user/0")
    assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_put_user_with_db():
    data = {'username': 'somename', 'email': 'email', 'password': 'password'}
    response = client.put(f"/user/{user_id}", content_type="application/json", data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.OK
    assert response.json["username"] == "somename"


def test_put_wrong_user_with_db():
    data = {'username': 'somename', 'password': 'password'}
    response = client.put(f"/user/{user_id}", content_type="application/json", data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_delete_user_with_db():
    response = client.delete(f"/user/{user_id}")
    assert response.status_code == http.HTTPStatus.NO_CONTENT


def test_delete_non_existent_user_with_db():
    response = client.delete(f"/user/{user_id}")
    assert response.status_code == http.HTTPStatus.NOT_FOUND
