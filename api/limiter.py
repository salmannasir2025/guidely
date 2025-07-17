import logging

import redis
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from .config import settings


def initialize_limiter():
    """Initializes the rate limiter, preferring Redis if available."""
    if settings.redis_url:
        try:
            # Test the connection before setting the limiter
            redis.from_url(settings.redis_url).ping()
            logging.info("Rate limiter configured with Redis storage.")
            return Limiter(key_func=get_remote_address, storage_uri=settings.redis_url)
        except redis.exceptions.ConnectionError as e:
            logging.warning(
                f"Could not connect to Redis for rate limiting ({e}). Falling back to in-memory storage."
            )
    logging.warning(
        "No REDIS_URL configured. Falling back to in-memory storage for rate limiting. Limits will NOT be shared across instances."
    )
    return Limiter(key_func=get_remote_address)


limiter = initialize_limiter()
default_rate_limit = "20/minute"
expensive_api_rate_limit = "10/minute"
