import http

from meeting_scheduler.src import app


def test_smoke():
    client = app.test_client()
    response = client.get("/smoke")
    assert response.status_code == http.HTTPStatus.OK
