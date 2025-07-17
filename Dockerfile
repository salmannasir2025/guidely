# --- Builder Stage ---
FROM python:3.11-slim as builder

# Create non-root user first
RUN groupadd -r app && useradd -r -g app app

# Ensure the user owns its own home directory (fixes permission error)
RUN mkdir -p /home/app && chown app:app /home/app

# Switch to non-root user
USER app

# Python env vars
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Copy requirement files and install everything
COPY requirements*.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-dev.txt

# --- Final Stage ---
FROM python:3.11-slim as final

# Re-create user in final stage
RUN groupadd -r app && useradd -r -g app app && \
    mkdir -p /home/app && chown app:app /home/app

USER app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Copy the pre-installed packages from the builder stage
COPY --from=builder /home/app/.local /home/app/.local
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy the application code
COPY --chown=app:app . .

# Default port for Cloud Run (can be overridden with -e PORT)
ENV PORT=8080

# Expose port
EXPOSE 8080

# Launch the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
