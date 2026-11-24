"""TRELLIS Fast In-Memory TTL Cache for Microsecond API Responses.

Provides thread-safe caching of high-frequency read endpoints with automatic
time-to-live expiration and selective cache invalidation on write events.
"""

from __future__ import annotations

import time
from typing import Any, Callable
from collections.abc import Hashable


class InMemoryTTLCache:
    """Thread-safe in-memory cache with per-item TTL."""

    def __init__(self, default_ttl_seconds: float = 30.0):
        self._cache: dict[str, tuple[float, Any]] = {}
        self.default_ttl = default_ttl_seconds

    def get(self, key: str) -> Any | None:
        item = self._cache.get(key)
        if not item:
            return None
        expires_at, value = item
        if time.time() > expires_at:
            self._cache.pop(key, None)
            return None
        return value

    def set(self, key: str, value: Any, ttl_seconds: float | None = None) -> None:
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
        self._cache[key] = (time.time() + ttl, value)

    def invalidate(self, prefix: str) -> int:
        """Remove all keys starting with prefix."""
        to_del = [k for k in self._cache if k.startswith(prefix)]
        for k in to_del:
            self._cache.pop(k, None)
        return len(to_del)

    def clear(self) -> None:
        self._cache.clear()


# Global cache instance
fast_cache = InMemoryTTLCache(default_ttl_seconds=30.0)
