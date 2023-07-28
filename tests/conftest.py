import pytest
from fastapi.testclient import TestClient

from app.core.database import get_db
from app.core.settings import settings
from app.main import app


@pytest.fixture(scope="class")
def token(client):
    response = client.post(
        f"api/v1/login?username={settings.DB_USER}&password={settings.DB_PASSWORD}"
    )
    return response.json()["access_token"]


@pytest.fixture(scope="class")
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="class")
def db_session():
    session = next(get_db())
    yield session
    session.close()


@pytest.fixture(scope="class")
def card_id(client, token):
    card_data = {
        "exp_date": "2024-07-01",
        "holder": "John Doe",
        "number": "4539578763621486",
        "cvv": "123",
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("api/v1/credit-card", headers=headers, json=card_data)
    assert response.status_code == 200
    return response.json()["id"]
