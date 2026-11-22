"""Optional Redis JSON cache used by the crop recommendation engine."""
from __future__ import annotations

import hashlib
import json
import logging
import os
from functools import lru_cache
from typing import Any

from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("CropVanta_Cache")


@lru_cache(maxsize=1)
def get_redis_client():
    redis_url = os.getenv("REDIS_URL", "").strip()
    if not redis_url:
        return None
    try:
        import redis
        client = redis.Redis.from_url(
            redis_url,
            decode_responses=True,
            socket_connect_timeout=2,
            socket_timeout=2,
            health_check_interval=30,
        )
        client.ping()
        logger.info("Redis cache connection established")
        return client
    except Exception as exc:
        logger.warning("Redis unavailable; inference will continue without Redis: %s", exc)
        return None


def build_cache_key(namespace: str, payload: Any) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return f"cropvanta:{namespace}:{digest}"


def get_cached_json(key: str):
    client = get_redis_client()
    if client is None:
        logger.info("Redis cache unavailable")
        return None

    try:
        value = client.get(key)

        if value:
            logger.info("REDIS CACHE HIT: %s", key)
            return json.loads(value)

        logger.info("REDIS CACHE MISS: %s", key)
        return None

    except Exception as exc:
        logger.warning("Redis read failed; continuing without cache: %s", exc)
        return None


def set_cached_json(key: str, value: Any, ttl_seconds: int = 3600) -> bool:
    client = get_redis_client()
    if client is None:
        return False
    try:
        client.setex(key, ttl_seconds, json.dumps(value, separators=(",", ":"), default=str))
        return True
    except Exception as exc:
        logger.warning("Redis write failed; continuing without cache: %s", exc)
        return False
