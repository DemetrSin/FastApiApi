import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from .films_api import app, get_session


@pytest.fixture(name='session')
def session_fixture():
    engine = create_engine(
        'sqlite://',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool
    )
    with Session(engine) as session:
        yield session


@pytest.fixture(name='client')
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_film(client: TestClient):
    response = client.post(
        '/films/',
        json={
            "film": {
                "name": "Infinite Journey",
                "release_date": "2024-07-15",
                "duration": 150,
                "description": "In a world where time is a commodity, a group of adventurers seeks to unlock the secrets of the universe.",
                "rating": 8.5
            },
            "producers": [
                {
                    "name": "Emily Smith"
                },
                {
                    "name": "Michael Johnson"
                }
            ],
            "actors": [
                {
                    "name": "Jessica Adams"
                },
                {
                    "name": "David Rodriguez"
                },
                {
                    "name": "Samuel Thompson"
                }
            ],
            "genres": [
                {
                    "name": "Science Fiction"
                },
                {
                    "name": "Adventure"
                },
                {
                    "name": "Drama"
                }
            ]
        }

    )
    data = response.json()
    assert response.status_code == 200
    assert data['film']['name'] == "Infinite Journey"
