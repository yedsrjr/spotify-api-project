from http import HTTPStatus

from spotify_api.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users/',
        json={'username': 'teste', 'password': 'teste123', 'email': 'teste@example.com'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'teste',
        'email': 'teste@example.com',
        'id': 1,
    }


def test_read_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


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


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'username': 'edson2', 'email': 'edson2@example.com', 'password': 'string'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user_with_wrong_user(client, other_user, token):
    response = client.delete(
        f'users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
