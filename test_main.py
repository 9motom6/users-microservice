import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base
import uuid
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def reset_app_lifespan():
    """Reset app state between tests."""
    yield


client = TestClient(app)


def test_create_user(test_db):
    external_id = str(uuid.uuid4())
    response = client.post(
        "/save",
        json={
            "external_id": external_id,
            "name": "testuser",
            "email": "testuser@example.com",
            "date_of_birth": "2021-01-01T12:00:00+00:00",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["name"] == "testuser"
    assert data["external_id"] == external_id


def test_create_user_duplicate_email(test_db):
    external_id = str(uuid.uuid4())
    client.post(
        "/save",
        json={
            "external_id": external_id,
            "name": "testuser",
            "email": "testuser@example.com",
            "date_of_birth": "2021-01-01T12:00:00+00:00",
        },
    )
    response = client.post(
        "/save",
        json={
            "external_id": str(uuid.uuid4()),
            "name": "testuser2",
            "email": "testuser@example.com",
            "date_of_birth": "2022-01-01T12:00:00+00:00",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}


def test_read_user(test_db):
    external_id = str(uuid.uuid4())
    response = client.post(
        "/save",
        json={
            "external_id": external_id,
            "name": "testuser",
            "email": "testuser@example.com",
            "date_of_birth": "2021-01-01T12:00:00+00:00",
        },
    )
    response = client.get(f"/users/{external_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["name"] == "testuser"
    assert data["external_id"] == external_id


def test_read_non_existent_user(test_db):
    response = client.get("/users/550e8400-e29b-41d4-a716-446655440000")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
