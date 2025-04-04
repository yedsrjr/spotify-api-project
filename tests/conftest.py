import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from spotify_api.app import app
from spotify_api.models import table_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metada.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)