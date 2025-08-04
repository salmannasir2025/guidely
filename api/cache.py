import functools
import hashlib
import json
import logging
from typing import Callable, Any

# In-memory cache dictionary
memory_cache = {}

def check_cache_connection() -> bool:
    """Checks if the cache is available."""
    return True  # In-memory cache is always available

def check_redis_connection() -> bool:
    """Checks if Redis cache is available (alias for check_cache_connection)."""
    return check_cache_connection()

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
                    logging.info(f"Cache HIT for {func.__name__}")
                    return cached_result

                logging.info(f"Cache MISS for {func.__name__}")
                result = await func(*args, **kwargs)
                memory_cache[cache_key] = result
                return result
            except Exception as e:
                logging.error(f"Cache error for {func.__name__}: {e}. Calling function directly.")
                return await func(*args, **kwargs)

        return wrapper

    return decorator

# Redis cache decorator fallback to memory cache
def redis_cache(ttl: int = 3600):
    """
    A decorator that mimics Redis cache behavior using in-memory cache.
    This provides compatibility for code expecting redis_cache decorator.
    """
    return memory_cache_decorator(ttl=ttl)

# Export redis_cache as a module-level variable for import compatibility
__all__ = ['redis_cache', 'check_cache_connection', 'check_redis_connection', 'memory_cache_decorator']
