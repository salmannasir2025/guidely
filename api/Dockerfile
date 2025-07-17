# --- Builder Stage ---
# This stage installs all dependencies, including development ones,
# creating a complete environment for testing or building.
FROM python:3.11-slim as builder
RUN groupadd -r app && useradd -r -g app app
USER app

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install all dependencies
COPY requirements*.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-dev.txt

# The builder stage has served its purpose. Now we start fresh with a clean
# production image to keep it small and secure.

# --- Final Stage ---
# This stage creates the lean production image.
FROM python:3.11-slim as final
RUN groupadd -r app && useradd -r -g app app
USER app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

WORKDIR /
WORKDIR /app

# Copy only the production dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy the application code from the current directory into the /app directory inside the container
COPY . .

# Command to run the application. Cloud Run will set the $PORT environment variable.
CMD ["uvicorn", "api.index:app", "--host", "0.0.0.0", "--port", "8080"]