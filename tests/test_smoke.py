import http


def test_smoke(test_client):
    response = test_client.get("/smoke")
    assert response.status_code == http.HTTPStatus.OK
