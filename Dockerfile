FROM python:3.14-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files first (better caching)
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

COPY src/ ./src/

ENV PYTHONPATH=/app/src

# Expose port
EXPOSE 8000

# Run the app
# Note: Pointing uvicorn to users-microservice.main:app
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]