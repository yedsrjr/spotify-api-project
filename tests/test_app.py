from http import HTTPStatus

from fastapi.testclient import TestClient

from spotify_api.app import app


def test_hello_world():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World!'}


def test_html_hello_world():
    client = TestClient(app)

    response = client.get('/ola-mundo')

    assert response.status_code == HTTPStatus.OK
    assert '<h1>Olá Mundo</h1>' in response.text
