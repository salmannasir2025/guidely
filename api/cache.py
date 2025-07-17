import functools
import hashlib
import json
import logging
from typing import Callable, Any
from fastapi.concurrency import run_in_threadpool

import redis
from .config import settings

# --- Redis Client Initialization ---
try:
    # from_url is convenient as it parses the connection string
    redis_client = redis.from_url(settings.redis_url, decode_responses=True)
    redis_client.ping()  # Check the connection
    logging.info("Successfully connected to Redis.")
except redis.exceptions.ConnectionError as e:
    logging.error(f"Failed to connect to Redis: {e}. Caching will be disabled.")
    redis_client = None


def check_redis_connection() -> bool:
    """Checks if the redis client is connected."""
    if not redis_client:
        return False
    try:
        # The PING command is lightweight and verifies the connection.
        return redis_client.ping()
    except redis.exceptions.RedisError:
        return False


def redis_cache(ttl: int = 3600):
    """
    An async-compatible decorator for caching function results in Redis.
    It assumes it is decorating an async function and uses a threadpool
    for non-blocking I/O with the synchronous redis-py client.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            if not redis_client:
                return await func(*args, **kwargs)

            # Create a stable cache key from the function's name and arguments
            arg_representation = json.dumps(
                (args, sorted(kwargs.items())), sort_keys=True
            )
            key_hash = hashlib.md5(arg_representation.encode()).hexdigest()
            cache_key = f"cache:{func.__name__}:{key_hash}"

            try:
                cached_result = await run_in_threadpool(redis_client.get, cache_key)
                if cached_result:
                    logging.info(f"Cache HIT for {func.__name__}")
                    return json.loads(cached_result)

                logging.info(f"Cache MISS for {func.__name__}")
                result = await func(*args, **kwargs)
                await run_in_threadpool(
                    redis_client.setex, cache_key, ttl, json.dumps(result)
                )
                return result
            except (redis.exceptions.RedisError, TypeError) as e:
                logging.error(
                    f"Redis cache error for {func.__name__}: {e}. Calling function directly."
                )
                return await func(*args, **kwargs)

        return wrapper

    return decorator
