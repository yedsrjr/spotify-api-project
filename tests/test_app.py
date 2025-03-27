from http import HTTPStatus


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
        '/users/',
        json={'username': 'teste', 'email': 'teste@example.com', 'password': 'teste123'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'teste',
        'email': 'teste@example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{'username': 'teste', 'email': 'teste@example.com', 'id': 1}]
    }


def test_update_user(client):
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
