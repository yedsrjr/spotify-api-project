from http import HTTPStatus

from fastapi.testclient import TestClient

from spotify_api.app import app


def test_hello_world():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World!'}
