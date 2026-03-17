# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /code

# Copy the dependency files
COPY pyproject.toml uv.lock /code/

# Install uv and dependencies
RUN pip install uv
RUN uv pip install --system --no-cache --frozen-lockfile

# Copy the application code
COPY ./app /code/app

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["uv", "run", "--host", "0.0.0.0", "fastapi", "dev", "app/main.py"]
