#!/usr/bin/python3

try:
    import memcache
except ImportError:
    pass

try:
    MEMCACHE_SERVERS = ["127.0.0.1:11211"]
    CACHE = memcache.Client(MEMCACHE_SERVERS, debug=0)
    CACHE_TTL = 60
except:
    CACHE = None

def get(key):
    """
    Retrieves a value for a given key in cache. This script assumes and uses memcache. Alternatively
    you can implement your own caching here. Caching is optional and should return "None" if no caching
    is enabled
    :param key: A string representing the key for a given key-value pair
    :return: The value for a given key-value pair. If it doesn't exists in cache it returns "None"
    Caching is optional and should return "None" if no caching is enabled
    """
    if CACHE is None:
        return None

    return CACHE.get(key)

def set(key, value, ttl=None):
    """
    Stores a key-value pair in cache. This script assumes and uses memcache. Alternatively you can
    implement your own caching here. Caching is optional and this method should return nothing
    if no caching is enabled
    :param key: A string representing the key for a given key-value pair
    :param value: The value for a given key-value pair
    :param ttl: How long in seconds a key-value pair should live in cache
    :return: If no cache client is found this method will simply return
    """
    if CACHE is None:
        return
    elif ttl is None:
        ttl = CACHE_TTL

    CACHE.set(key, value, ttl)