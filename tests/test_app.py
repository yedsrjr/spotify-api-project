from http import HTTPStatus

from spotify_api.schemas import UserPublic


def test_hello_world(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World!'}


def test_html_hello_world(client):
    response = client.get('/ola-mundo')

    assert response.status_code == HTTPStatus.OK
    assert '<h1>Olá Mundo</h1>' in response.text


def test_create_user(client):
    response = client.post(
        '/users',
        json={'username': 'teste', 'password': 'teste123', 'email': 'teste@teste.com'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'teste',
        'email': 'teste@teste.com',
        'id': 1,
    }


def test_read_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={'username': 'edson', 'email': 'edson@gmail.com', 'password': 'senha123'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'username': 'edson', 'email': 'edson@gmail.com', 'id': 1}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}
