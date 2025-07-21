# Test commit to verify Cloud Build trigger
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse, StreamingResponse
import asyncio
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from . import cache, config, database, llm, logging_config, ocr, speech
from .routers import ask, data, auth, utils  # Import the router modules
from .limiter import _rate_limit_exceeded_handler, limiter
from .schemas import ComponentStatus, HealthCheckResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on application startup
    logging_config.setup_logging()
    llm.initialize_llm()
    database.initialize_database()
    ocr.initialize_ocr_client()
    speech.initialize_speech_clients()
    yield
    # Code to run on application shutdown (e.g., close connections)
    logging.info("Application shutdown.")


# --- Application Setup ---
app = FastAPI(
    title="AI Tutor & Assistant API",
    description="Backend for the AI Tutor and Assistant for Pakistan.",
    version="0.1.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# --- Middleware ---
# Add CORS middleware to allow the frontend to communicate with the backend.
# In a production environment, you would restrict the origins to your frontend's domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.settings.frontend_url],
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "OPTIONS",
    ],  # Restrict to only the methods your frontend uses
    allow_headers=[
        "Content-Type",
        "Authorization",
    ],  # Restrict to only the headers your frontend sends
)

# --- API Routers ---
app.include_router(auth.router)
app.include_router(ask.router)
app.include_router(data.router)
app.include_router(utils.router)


@app.get("/", tags=["Monitoring"])
async def read_root():
    """A simple endpoint to confirm the API is running."""
    return {"message": "Welcome to the AI Tutor & Assistant API!"}


@app.get("/health", response_model=HealthCheckResponse, tags=["Monitoring"])
async def health_check(response: Response):
    """
    Performs a health check on the API and its critical dependencies.
    Returns 200 OK if all critical services are up, otherwise 503 Service Unavailable.
    """
    # Define all health checks in a list for easy extension
    checks = [
        ("database", database.check_db_connection, "Could not connect to MongoDB."),
        ("redis_cache", cache.check_redis_connection, "Could not connect to Redis."),
        ("llm_service", llm.check_llm_client, "LLM client not initialized."),
        (
            "vision_service",
            ocr.check_vision_client,
            "Google Vision client not initialized.",
        ),
        (
            "speech_to_text_service",
            speech.check_speech_to_text_client,
            "Google Speech-to-Text client not initialized.",
        ),
        (
            "text_to_speech_service",
            speech.check_text_to_speech_client,
            "Google Text-to-Speech client not initialized.",
        ),
    ]

    component_statuses: dict = {}
    is_healthy = True

    for name, check_func, error_details in checks:
        # This handles both regular functions and async functions
        if asyncio.iscoroutinefunction(check_func):
            ok = await check_func()
        else:
            ok = check_func()

        if ok:
            component_statuses[name] = ComponentStatus(status="ok")
        else:
            is_healthy = False
            component_statuses[name] = ComponentStatus(
                status="error", details=error_details
            )

    overall_status = "ok" if is_healthy else "error"
    status_code = 200 if is_healthy else 503

    response.status_code = status_code
    return HealthCheckResponse(status=overall_status, components=component_statuses)


if __name__ == "__main__":
    import uvicorn

    # This block allows running the app directly for local development
    # e.g., `python -m backend.main` from the root directory
    uvicorn.run(app, host="127.0.0.1", port=8000)
