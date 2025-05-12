from dataclasses import asdict

import pytest
from sqlalchemy import select

from spotify_api.models import User


@pytest.mark.asyncio
async def test_create_db_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='edson.junior', password='minha_senha', email='edsonr@gmail.com'
        )
        session.add(new_user)
        await session.commit()

    user = await session.scalar(select(User).where(User.username == 'edson.junior'))

    assert asdict(user) == {
        'id': 1,
        'username': 'edson.junior',
        'password': 'minha_senha',
        'email': 'edsonr@gmail.com',
        'created_at': time,
        'updated_at': time,
    }
