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
        json={'username': 'teste', 'password': 'teste123', 'email': 'teste@example.com'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'teste',
        'email': 'teste@example.com',
        'id': 1,
    }


def test_create_user_already_exists(client, user):
    response = client.post(
        '/users',
        json={'username': 'teste', 'email': 'example@example.com', 'password': 'teste123'},
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'User already exists'}


def test_create_user_with_email_already_exists(client, user):
    response = client.post(
        '/users',
        json={'username': 'edsen', 'email': 'teste@example.com', 'password': 'teste123'},
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


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


def test_update_user_not_found(client, user):
    response = client.put(
        '/users/2',
        json={'username': 'edson', 'email': 'edsen@gmail.com', 'password': '123eds'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_integrity_error(client, user):
    client.post(
        '/users',
        json={'username': 'aleatorio', 'email': 'aleatorio@example.com', 'password': 'ale123'},
    )

    response_update = client.put(
        f'users/{user.id}',
        json={
            'username': 'aleatorio',
            'email': 'integrity@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {'detail': 'Username or Email already exists'}


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_not_found(client, user):
    response = client.delete('/users/2')
    
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
