# Test commit to verify Cloud Build trigger
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse, StreamingResponse
import asyncio
import os
import logging
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from . import cache, config, database, llm, logging_config
from .tools.registry import tool_registry
from .routers import ask, data, auth, utils, files
from .limiter import _rate_limit_exceeded_handler, limiter
from .schemas import ComponentStatus, HealthCheckResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on application startup
    logging_config.setup_logging()
    llm.initialize_llm()
    database.initialize_database()
    cache.initialize_redis()  # Initialize Redis client
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
    allow_origins=config.settings.allowed_origins + [config.settings.frontend_url],
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "DELETE",
        "PUT",
        "OPTIONS",
    ],  # Restrict to only the methods your frontend uses
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
    ],  # Restrict to only the headers your frontend sends
)

# --- API Routers ---
# Update the import line
from .routers import ask, data, auth, utils, files, user_keys  # Add user_keys to the import

# Update the router registration section
app.include_router(auth.router)
app.include_router(ask.router)
app.include_router(data.router)
app.include_router(utils.router)
app.include_router(files.router)
app.include_router(user_keys.router)  # Add the user_keys router


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
        ("llm_service", llm.check_llm_client, "LLM provider not initialized."),
    ]

    # Dynamically add registered tools to health checks
    for tool_name in tool_registry.list_tools():
        tool = tool_registry.get_tool(tool_name)
        checks.append((
            f"tool_{tool_name}", 
            lambda t=tool: t is not None, 
            f"Tool {tool_name} not available."
        ))

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
    import os
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
