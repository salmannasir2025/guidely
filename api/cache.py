import functools
import hashlib
import json
import logging
import os
from typing import Callable, Any, Optional
import redis.asyncio as redis
from .config import settings

# Redis client
redis_client: Optional[redis.Redis] = None

# In-memory cache dictionary (fallback)
memory_cache = {}

# Initialize Redis client if REDIS_URL is available
def initialize_redis():
    """Initialize Redis client if REDIS_URL is available."""
    global redis_client
    try:
        if settings.redis_url:
            logging.info("Initializing Redis client...")
            redis_client = redis.from_url(settings.redis_url, decode_responses=True)
            logging.info("Redis client initialized successfully.")
        else:
            logging.warning("REDIS_URL not set. Using in-memory cache as fallback.")
    except Exception as e:
        logging.error(f"Failed to initialize Redis client: {e}. Using in-memory cache as fallback.")

async def check_cache_connection() -> bool:
    """Checks if the cache is available."""
    if redis_client:
        try:
            await redis_client.ping()
            return True
        except Exception:
            return False
    return True  # In-memory cache is always available

async def check_redis_connection() -> bool:
    """Checks if Redis cache is available."""
    if redis_client:
        try:
            await redis_client.ping()
            return True
        except Exception:
            return False
    return False  # Redis is not available

def memory_cache_decorator(ttl: int = 3600):
    """
    A decorator for caching function results in an in-memory dictionary.
    It assumes it is decorating an async function.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # Create a stable cache key from the function's name and arguments
            arg_representation = json.dumps((args, sorted(kwargs.items())), sort_keys=True)
            key_hash = hashlib.md5(arg_representation.encode()).hexdigest()
            cache_key = f"cache:{func.__name__}:{key_hash}"

            try:
                cached_result = memory_cache.get(cache_key)
                if cached_result:
                    logging.info(f"Memory Cache HIT for {func.__name__}")
                    return cached_result

                logging.info(f"Memory Cache MISS for {func.__name__}")
                result = await func(*args, **kwargs)
                memory_cache[cache_key] = result
                return result
            except Exception as e:
                logging.error(f"Memory Cache error for {func.__name__}: {e}. Calling function directly.")
                return await func(*args, **kwargs)

        return wrapper

    return decorator

def redis_cache(ttl: int = 3600):
    """
    A decorator for caching function results in Redis.
    Falls back to in-memory cache if Redis is not available.
    It assumes it is decorating an async function.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # Create a stable cache key from the function's name and arguments
            arg_representation = json.dumps((args, sorted(kwargs.items())), sort_keys=True)
            key_hash = hashlib.md5(arg_representation.encode()).hexdigest()
            cache_key = f"cache:{func.__name__}:{key_hash}"

            # Use Redis if available, otherwise fall back to memory cache
            if redis_client:
                try:
                    # Try to get from Redis
                    cached_result = await redis_client.get(cache_key)
                    if cached_result:
                        logging.info(f"Redis Cache HIT for {func.__name__}")
                        return json.loads(cached_result)

                    logging.info(f"Redis Cache MISS for {func.__name__}")
                    result = await func(*args, **kwargs)
                    
                    # Store in Redis with expiration
                    await redis_client.set(
                        cache_key,
                        json.dumps(result, default=str),  # Use default=str to handle non-serializable objects
                        ex=ttl
                    )
                    return result
                except Exception as e:
                    logging.error(f"Redis Cache error for {func.__name__}: {e}. Falling back to memory cache.")
                    # Fall back to memory cache
                    return await memory_cache_wrapper(*args, **kwargs)
            else:
                # Use memory cache
                return await memory_cache_wrapper(*args, **kwargs)
                
        # Inner memory cache wrapper for fallback
        async def memory_cache_wrapper(*args, **kwargs) -> Any:
            arg_representation = json.dumps((args, sorted(kwargs.items())), sort_keys=True)
            key_hash = hashlib.md5(arg_representation.encode()).hexdigest()
            cache_key = f"cache:{func.__name__}:{key_hash}"
            
            cached_result = memory_cache.get(cache_key)
            if cached_result:
                logging.info(f"Memory Cache HIT for {func.__name__}")
                return cached_result

            logging.info(f"Memory Cache MISS for {func.__name__}")
            result = await func(*args, **kwargs)
            memory_cache[cache_key] = result
            return result

        return wrapper

    return decorator

# Export functions as module-level variables for import compatibility
__all__ = ['redis_cache', 'check_cache_connection', 'check_redis_connection', 'memory_cache_decorator', 'initialize_redis']
