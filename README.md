# 👤 Users Microservice

A streamlined, production-ready microservice for managing user records, built with **FastAPI**, **SQLAlchemy**, and **Pydantic v2**.

The app is deployed at [https://users-microservice.444424444.xyz](https://users-microservice.444424444.xyz/docs)

---

## 🛠️ Project Architecture

| File | Purpose |
| :--- | :--- |
| **`src/app/main.py`** | Entry point, FastAPI app setup, and API routing. |
| **`src/app/crud.py`** | Create, Read, logic (Update, Delete could be added later). |
| **`src/app/models.py`** | SQLAlchemy database models (The "Database" layer). |
| **`src/app/schemas.py`** | Pydantic validation models (The "API" layer). |
| **`src/app/database.py`** | Engine configuration and session management. |
| **`tests/`** | Comprehensive integration and unit test suite. |

---

## 🚀 Getting Started

This project uses [uv](https://github.com/astral-sh/uv) for lightning-fast dependency management.

### 1. Installation
Clone the repository and sync the environment:
```bash
# Install dependencies and create a virtual environment automatically
uv sync
```

### 2. Running the Application
Launch the development server with hot-reload enabled:
```bash
uv run fastapi dev src/app/main.py
```
The API will be available at **`http://localhost:8000`**.

### 3. Running Tests
Execute the test suite (includes database integration tests):
```bash
uv run pytest
```

---

## 🐳 Docker Deployment

The included `Dockerfile` is optimized to use `uv` for minimal build times and small image footprints.

```bash
# Build the image
docker build -t users-microservice .

# Run the container
docker run -p 8000:8000 users-microservice
```

---

## 📡 API Reference

Once the server is running, you can explore the interactive documentation:
* **Swagger UI (Interactive):** `http://localhost:8000/docs`
* **ReDoc:** `http://localhost:8000/redoc`

### Key Endpoints

#### **Create a User**
`POST /save`
```bash
curl -X POST "http://localhost:8000/save" \
     -H "Content-Type: application/json" \
     -d '{
       "external_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
       "name": "John Doe",
       "email": "john.doe@example.com",
       "date_of_birth": "1990-01-01T12:00:00"
     }'
```

#### **Retrieve a User**
`GET /{external_id}`
```bash
curl -X GET "http://localhost:8000/a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
```

---

## 🛠️ Development Tools
* **Formatting/Linting:** This project is compatible with `ruff`.
* **Database:** Uses **SQLite** by default (local file `users.db`).
* **ID System:** Uses **UUIDv4** for `external_id` as the primary lookup key.
