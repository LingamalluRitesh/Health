"""
HealthPulse AI — High Performance In-Memory TTL Cache.
Provides fast caching for patient EHR lookups and clinical score calculation results.
"""

import time
from typing import Dict, Any, Optional, Tuple


class TTLCache:
    """Thread-safe In-Memory Key-Value Store with Time-To-Live expiration."""

    def __init__(self, default_ttl_sec: int = 300):
        self.default_ttl_sec = default_ttl_sec
        self._store: Dict[str, Tuple[Any, float]] = {}

    def get(self, key: str) -> Optional[Any]:
        if key not in self._store:
            return None
        value, expiry = self._store[key]
        if time.time() > expiry:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any, ttl_sec: Optional[int] = None) -> None:
        duration = ttl_sec if ttl_sec is not None else self.default_ttl_sec
        expiry = time.time() + duration
        self._store[key] = (value, expiry)

    def delete(self, key: str) -> bool:
        if key in self._store:
            del self._store[key]
            return True
        return False

    def clear(self) -> None:
        self._store.clear()

    def size(self) -> int:
        now = time.time()
        expired = [k for k, (_, exp) in self._store.items() if now > exp]
        for k in expired:
            del self._store[k]
        return len(self._store)


global_cache = TTLCache()
