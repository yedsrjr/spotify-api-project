from sqlalchemy import select
from dataclasses import asdict

from spotify_api.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='edson.junior', password='minha_senha', email='edsonr@gmail.com'
        )
        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == 'edson.junior'))

    assert asdict(user) == {
        'id': 1,
        'username': 'edson.junior',
        'password': 'minha_senha',
        'email': 'edsonr@gmail.com',
        'created_at': time,
        'created_at': time
    }
