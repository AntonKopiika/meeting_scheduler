import http
import json


def test_get_users_with_db(test_client):
    response = test_client.get("/user")
    assert response.status_code == http.HTTPStatus.OK


def test_post_user_with_db(test_client):
    data = {'username': "testuser5", 'email': "user_email", 'password': "user_password"}
    response = test_client.post("/user", content_type="application/json", data=json.dumps(data))
    assert response.status_code == http.HTTPStatus.CREATED
    assert response.json["username"] == "testuser5"
    assert response.json["email"] == "user_email"


def test_post_wrong_data_user_with_db(test_client):
    data = {'name': 'username'}
    response = test_client.post("/user", content_type="application/json", data=json.dumps(data))
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_get_user_by_id_with_db(test_client, test_user):
    response = test_client.get(f"/user/{test_user.id}")
    assert response.status_code == http.HTTPStatus.OK
    assert response.json["username"] == test_user.username
    assert response.json["email"] == test_user.email


def test_get_non_existent_user_with_db(test_client):
    response = test_client.get(f"/user/0")
    assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_put_user_with_db(test_client, test_user):
    data = {'username': 'testuser12', 'email': 'someemail', 'password': 'password'}
    response = test_client.put(f"/user/{test_user.id}", content_type="application/json", data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.OK
    assert response.json["username"] == "testuser12"


def test_put_wrong_user_with_db(test_client, test_user):
    data = {'username': 'somename', 'password': 'password'}
    response = test_client.put(f"/user/{test_user.id}", content_type="application/json", data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_delete_non_existent_user_with_db(test_client):
    response = test_client.delete(f"/user/0")
    assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_delete_user_with_db(test_client, test_user):
    response = test_client.delete(f"/user/{test_user.id}")
    assert response.status_code == http.HTTPStatus.NO_CONTENT
