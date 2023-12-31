from django.conf import settings
from django.core.cache import cache
from functools import wraps
# from django.views.decorators.cache import


def cache_with_args(caching_method, key: str):  # to pass arguments in the decorator
    def cache_this(django_method):  # Here is where the cache_this decorator takes
        @wraps(django_method)
        def wrapper(*args, **kwargs):
            return django_method(*args, **kwargs)
        return wrapper
    cache.set(key, cache_this)
    return cache_this


# def cache_this(django_method, key=None):  # Here is where the cache_this decorator takes argument 'key' to set the value in the cache as key
#     def wrapper(*args, **kwargs):
#         return django_method(*args, **kwargs)
#
#     cache.set('key', wrapper)
#     return wrapper


def cache_this(django_method):
    @wraps(django_method)
    def wrapper(*args, **kwargs):
        # Generate a cache key based on the function name and arguments
        cache_key = f"{django_method.__name__}:{str(args)}:{str(kwargs)}"
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            cache.touch(settings.CACHE_TOUCH_TTL)
            return cached_result
        result = django_method(*args, **kwargs)
        cache.set(cache_key, result)
        return result
    return wrapper

# from redis.connection import
# @cache_this
# def print_hi(value):
#     return f'the value is {value}'
