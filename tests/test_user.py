import http
import json
from dataclasses import dataclass
from unittest.mock import patch
from meeting_scheduler.src.db_service import CRUDService

user_id = 0


@dataclass
class TestUser:
    username = "username"
    email = "test@mail.com"
    password = "testpasswd"


def test_get_users_with_db(test_client):
    response = test_client.get("/user")
    assert response.status_code == http.HTTPStatus.OK


def test_get_users_mock_db(test_client):
    with patch.object(CRUDService, "get_all", return_value=[]) as mock_get_users:
        response = test_client.get("/user")
        mock_get_users.assert_called_once()
        assert response.json == []


def test_post_user_with_db(test_client, test_users):
    user = test_users[0]
    data = {'username': user.username, 'email': user.email, 'password': user.password}
    response = test_client.post("/user", content_type="application/json", data=json.dumps(data))
    assert response.status_code == http.HTTPStatus.CREATED
    assert response.json["username"] == user.username
    assert response.json["email"] == user.email
    global user_id
    user_id = response.json["id"]


def test_post_user_mock_db(test_client, test_users):
    with patch.object(CRUDService, "add") as mock_add_user:
        user = test_users[0]
        data = {'username': user.username, 'email': user.email, 'password': user.password}
        response = test_client.post("/user", content_type="application/json", data=json.dumps(data))
        mock_add_user.assert_called_once()


def test_post_wrong_data_user_with_db(test_client):
    data = {'name': 'username'}
    response = test_client.post("/user", content_type="application/json", data=json.dumps(data))
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_get_user_by_id_with_db(test_client, test_users):
    response = test_client.get(f"/user/{user_id}")
    assert response.status_code == http.HTTPStatus.OK
    assert response.json["username"] == test_users[0].username


def test_get_user_mock_db(test_client, test_users):
    with patch.object(CRUDService, "get", return_value=TestUser()) as mock_get_user:
        response = test_client.get(f"/user/{user_id}")
        mock_get_user.assert_called_once()
        assert response.json["username"] == "username"


def test_get_non_existent_user_with_db(test_client):
    response = test_client.get(f"/user/0")
    assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_put_user_with_db(test_client):
    data = {'username': 'somename', 'email': 'someemail', 'password': 'password'}
    response = test_client.put(f"/user/{user_id}", content_type="application/json", data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.OK
    assert response.json["username"] == "somename"


def test_put_user_mock_db(test_client):
    with patch.object(CRUDService, "get", return_value=TestUser()) as mock_get_user, \
            patch.object(CRUDService, "update") as mock_put_user:
        data = {'username': 'somename', 'email': 'someemail', 'password': 'password'}
        response = test_client.put(f"/user/{user_id}", content_type="application/json", data=json.dumps(data))
        mock_get_user.assert_called_once()
        mock_put_user.assert_called_once()


def test_put_wrong_user_with_db(test_client):
    data = {'username': 'somename', 'password': 'password'}
    response = test_client.put(f"/user/{user_id}", content_type="application/json", data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_delete_user_with_db(test_client):
    response = test_client.delete(f"/user/{user_id}")
    assert response.status_code == http.HTTPStatus.NO_CONTENT


def test_delete_user_mock_db(test_client):
    with patch.object(CRUDService, "get", return_value=TestUser()) as mock_get_user, \
            patch.object(CRUDService, "delete") as mock_delete_user:
        response = test_client.delete(f"/user/{user_id}")
        mock_get_user.assert_called_once()
        mock_delete_user.assert_called_once()


def test_delete_non_existent_user_with_db(test_client):
    response = test_client.delete(f"/user/{user_id}")
    assert response.status_code == http.HTTPStatus.NOT_FOUND
