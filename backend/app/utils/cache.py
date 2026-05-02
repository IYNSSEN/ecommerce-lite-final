import time

_cache = {}


def get_cache(key):
    item = _cache.get(key)
    if not item:
        return None
    value, expires_at = item
    if time.time() > expires_at:
        _cache.pop(key, None)
        return None
    return value


def set_cache(key, value, ttl_seconds=60):
    _cache[key] = (value, time.time() + ttl_seconds)


def invalidate_prefix(prefix):
    for key in list(_cache.keys()):
        if key.startswith(prefix):
            _cache.pop(key, None)
