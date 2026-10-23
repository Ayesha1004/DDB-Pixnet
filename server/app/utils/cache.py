import os
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"

_pool = redis.ConnectionPool.from_url(
    REDIS_URL, max_connections=100, socket_timeout=0.5, socket_connect_timeout=0.5
)
_client = redis.Redis(connection_pool=_pool)


def cache_get(key: str):
    if not CACHE_ENABLED:
        return None
    try:
        return _client.get(key)
    except redis.RedisError:
        return None  # Redis down -> fall through to Postgres, never fail the request


def cache_set(key: str, value: str, ttl: int) -> None:
    if not CACHE_ENABLED:
        return
    try:
        _client.set(key, value, ex=ttl)
    except redis.RedisError:
        pass


def cache_delete(*keys: str) -> None:
    if not CACHE_ENABLED:
        return
    try:
        _client.delete(*keys)
    except redis.RedisError:
        pass