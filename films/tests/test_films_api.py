import pytest
import json
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from films.films_api import app, get_session


def load_test_payload():
    with open('tests/test_films_payload.json', 'r') as file:
        return json.load(file)


@pytest.fixture(name='session')
def session_fixture():
    engine = create_engine(
        'sqlite://',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
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


# POST Film

def test_create_film_successful(client: TestClient):
    payload = load_test_payload()
    response = client.post('/films/', json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == "Infinite Journey"
    assert data['genres'][0]['name'] == "Science Fiction"


def test_create_film_missing_entities(client: TestClient):
    payload = load_test_payload()
    payload.pop('producers')
    payload.pop('actors')
    response = client.post('/films/', json=payload)
    assert response.status_code == 422


def test_create_film_invalid_genre_type(client: TestClient):
    payload = load_test_payload()
    payload['genres'] = {"name": "Invalid Genre"}
    response = client.post('/films/', json=payload)
    assert response.status_code == 422


def test_create_film_empty_payload(client: TestClient):
    response = client.post('/films/', json={})
    assert response.status_code == 422


# GET Film/id


def test_get_film_successful(client: TestClient):
    payload = load_test_payload()
    response = client.post('/films/', json=payload)
    assert response.status_code == 200
    data = response.json()
    film_id = data['id']

    response = client.get(f'/films/{film_id}')
    assert response.status_code == 200


def test_get_non_existent_film(client: TestClient):
    response = client.get('/films/999999')
    assert response.status_code == 404


def test_get_film_invalid_id_format(client: TestClient):
    response = client.get('/films/sssss')
    assert response.status_code == 404


# GET Films

def test_get_films_successful(client: TestClient):
    payload = load_test_payload()
    client.post('/films/', json=payload)

    response = client.get('/films/')
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1


def test_get_films_with_offset_and_limit(client: TestClient):
    payload = load_test_payload()
    client.post('/films/', json=payload)

    response = client.get('/films/?offset=5&limit=8')
    assert response.status_code == 404
    data = response.json()

    assert len(data) == 1


def test_get_films_with_invalid_limit(client: TestClient):
    response = client.get('/films/?limit=15')
    assert response.status_code == 422


def test_get_films_with_invalid_offset(client: TestClient):
    response = client.get('/films/?offset=-5')
    assert response.status_code == 404
