"""
Integration tests - runs the application as close to production as possible.
Uses a temporary SQLite database file and overrides the FastAPI dependency.
"""

import os
import pytest
import uuid
import tempfile
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base


@pytest.fixture(scope="module")
def engine():
    """Create a temporary database file and SQLAlchemy engine."""
    # mktemp is safer on Windows to avoid "File in use" errors during setup
    db_path = tempfile.mktemp(suffix=".db")
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )

    # Create the tables in the temporary database
    Base.metadata.create_all(bind=engine)

    yield engine

    # Teardown: Close all connections and attempt to delete the file
    engine.dispose()
    try:
        if os.path.exists(db_path):
            os.remove(db_path)
    except PermissionError:
        # On Windows, sometimes the OS holds the handle a bit longer
        print(f"\nCleanup Note: Temp DB at {db_path} will be deleted by OS later.")


@pytest.fixture(scope="function")
def db_session(engine):
    """Provides a clean database session for every test function."""
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    # Cleanup session and rollback any uncommitted changes to keep tests isolated
    session.close()
    if transaction.is_active:
        transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """
    Overrides the 'get_db' dependency in the FastAPI app to use
    the current test's database session.
    """

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

    # Clear overrides so they don't affect other test files
    app.dependency_overrides.clear()


# --- Test Cases ---


def test_create_and_read_user_integration(client):
    """Test the full flow: create a user and then retrieve them by ID."""
    external_id = str(uuid.uuid4())
    user_payload = {
        "external_id": external_id,
        "name": "Integration Tester",
        "email": "test@integration.com",
        "date_of_birth": "1995-05-15T00:00:00",
    }

    # 1. Save User
    save_res = client.post("/save", json=user_payload)
    assert save_res.status_code == 200

    # 2. Get User (ensure the path matches your app.get("/{user_id}") route)
    get_res = client.get(f"/users/{external_id}")
    assert get_res.status_code == 200

    data = get_res.json()
    assert data == user_payload


def test_duplicate_email_integration(client):
    """Verify that the system prevents duplicate emails using IntegrityError logic."""
    shared_email = "duplicate@example.com"

    # Create first user
    client.post(
        "/save",
        json={
            "external_id": str(uuid.uuid4()),
            "name": "User One",
            "email": shared_email,
            "date_of_birth": "1990-01-01T00:00:00",
        },
    )

    # Try to create second user with same email
    response = client.post(
        "/save",
        json={
            "external_id": str(uuid.uuid4()),
            "name": "User Two",
            "email": shared_email,
            "date_of_birth": "1992-01-01T00:00:00",
        },
    )

    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_read_nonexistent_user_integration(client):
    """Verify 404 behavior for IDs that don't exist."""
    random_id = str(uuid.uuid4())
    response = client.get(f"/users/{random_id}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
