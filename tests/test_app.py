from http import HTTPStatus

from spotify_api.schemas import UserPublic
from spotify_api.security import create_access_token


def test_hello_world(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World!'}


def test_html_hello_world(client):
    response = client.get('/ola-mundo')

    assert response.status_code == HTTPStatus.OK
    assert '<h1>Olá Mundo</h1>' in response.text


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_get_token_user_not_found(client, user):
    response = client.post(
        '/token', data={'username': 'teste@teste', 'password': user.password}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


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
        json={
            'username': user.username,
            'email': 'example@example.com',
            'password': 'teste123',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'User already exists'}


def test_create_user_with_email_already_exists(client, user):
    response = client.post(
        '/users', json={'username': 'edsen', 'email': user.email, 'password': 'teste123'}
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user_with_id(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'teste',
        'email': 'teste@example.com',
        'id': user.id,
    }


def test_read_user_with_id_not_found(client):
    response = client.get('users/254')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'username': 'edson', 'email': 'edson@gmail.com', 'password': 'senha123'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'username': 'edson', 'email': 'edson@gmail.com', 'id': user.id}


def test_update_integrity_error(client, user, token):
    client.post(
        '/users',
        json={
            'username': 'aleatorio',
            'email': 'aleatorio@example.com',
            'password': 'ale123',
        },
    )

    response_update = client.put(
        f'users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'aleatorio',
            'email': 'integrity@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {'detail': 'Username or Email already exists'}


def test_delete_user(client, user, token):
    response = client.delete(f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_get_current_user_credentials_exception(client):
    data = {'no-email': 'test'}
    token = create_access_token(data)

    response = client.delete('/users/1', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_not_found_credentials_exception(client):
    data = {'sub': 'test@test'}
    token = create_access_token(data)

    response = client.delete('/users/1', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
