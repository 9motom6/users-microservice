# Users Microservice

This is a simple microservice for managing users, built with FastAPI.

## Project Structure

- `app/main.py`: The main FastAPI application logic.
- `app/crud.py`: Contains functions for database operations.
- `app/database.py`: Database connection and session management.
- `app/models.py`: SQLAlchemy models for the database tables.
- `app/schemas.py`: Pydantic schemas for data validation.
- `Dockerfile`: For building the Docker image.
- `test_main.py`: Integration tests.

## How to Run

1.  **Install dependencies:**
    ```bash
    pip install uv
    uv pip install -e ".[dev]"
    ```

2.  **Run the application:**
    ```bash
    uv run fastapi dev app/main.py
    ```
    The application will be available at `http://localhost:8000`.

## How to Run with Docker

1.  **Build the Docker image:**
    ```bash
    docker build -t users-microservice .
    ```

2.  **Run the Docker container:**
    ```bash
    docker run -p 8000:8000 users-microservice
    ```

## How to Run Tests

```bash
uv run pytest
```

## API Usage

### Create a user

```bash
curl -X POST "http://localhost:8000/save" -H "Content-Type: application/json" -d '{
"external_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
"name": "John Doe",
"email": "john.doe@example.com",
"date_of_birth": "1990-01-01T12:00:00+00:00"
}'
```

### Get a user by ID

```bash
curl -X GET "http://localhost:8000/1"
```
