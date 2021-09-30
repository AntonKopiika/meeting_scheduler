import http
import json


def test_get_accounts_with_db(test_client):
    response = test_client.get("/user/account")
    assert response.status_code == http.HTTPStatus.OK


def test_post_account_with_db(test_client, test_user):
    data = {
        'email': "testuser@gmail.com",
        'cred': "3453dfhf54yhd35wr57",
        "provider": "google",
        "description": "",
        "user": test_user.id
    }
    response = test_client.post("/user/account", content_type="application/json", data=json.dumps(data))
    assert response.status_code == http.HTTPStatus.CREATED
    assert response.json["email"] == "testuser@gmail.com"


def test_post_wrong_data_account_with_db(test_client):
    data = {'name': 'username'}
    response = test_client.post("/user/account", content_type="application/json", data=json.dumps(data))
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_get_account_by_id_with_db(test_client, test_account):
    response = test_client.get(f"/user/account/{test_account.id}")
    assert response.status_code == http.HTTPStatus.OK
    assert response.json["email"] == test_account.email


def test_get_non_existent_account_with_db(test_client):
    response = test_client.get(f"/user/account/0")
    assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_put_account_with_db(test_client, test_account, test_user):
    data = {
        'email': "testuser21@gmail.com",
        'cred': "3453dfhf54",
        "provider": "google",
        "description": "description",
        'user': test_user.id,
    }
    response = test_client.put(f"/user/account/{test_account.id}", content_type="application/json", data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.OK


def test_put_wrong_account_with_db(test_client, test_account):
    data = {'username': 'somename'}
    response = test_client.put(f"/user/account/{test_account.id}", content_type="application/json", data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_delete_non_existent_account_with_db(test_client):
    response = test_client.delete(f"/user/account/0")
    assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_delete_account_with_db(test_client, test_account):
    response = test_client.delete(f"/user/account/{test_account.id}")
    assert response.status_code == http.HTTPStatus.NO_CONTENT
