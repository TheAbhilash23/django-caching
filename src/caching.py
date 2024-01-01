from django.conf import settings
from django.core.cache import cache
from functools import wraps
# from django.views.decorators.cache import

global CACHE_IMPLEMENTATIONS
CACHE_IMPLEMENTATIONS = (
    ('DIRECT_SET', (
        'profiles.views.ProfileViewSet.list',
    )
     ),
    ('INDIRECT_SET', (
        'profiles.views.ProfileViewSet.list'
    )
     ),
)


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


def cache_this_for_client_session(django_method):
    @wraps(django_method)
    def wrapper(*args, **kwargs):
        # Generate a cache key based on the function name and arguments
        # use wisely because invalidation is based only on TTL.
        # That is why keep TTL for it at a low value supposedly for a user session length only
        # and since touch method will reset the time, session length being token length
        # and assuming 5 hits per session for the method we can keep the ttl to around 1 min.

        cache_key = f"{django_method.__name__}:{str(args)}:{str(kwargs)}"
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            cache.touch(settings.CACHE_OBJECT_TOUCH_CLIENT_SESSION)
            return cached_result
        result = django_method(*args, **kwargs)
        cache.set(cache_key, result)
        return result
    return wrapper

# from redis.connection import
# @cache_this
# def print_hi(value):
#     return f'the value is {value}'


def invalidatable_cache(*args):
    """
    Use this decorator over methods which persist data in db one form or another.
    Pass the relevant args kwargs to the decorator to save the data as a combination for the key on
    the cache, here know as cache_key.
    This is the side cache we can use to store data on cache and since the keys are provided
    while executing, we can use the keys to reset where the data is updated.

    Cache method must be listed in {decorator.__module__} CACHE_IMPLEMENTATIONS '
    to avoid speghettification, in DIRECT_SET
    """
    def decorator(func):
        @wraps(func)
        def wrapper_method(*func_args, **func_kwargs):
            validate_listing = f'{func.__module__}.{func.__qualname__}'
            # assert validate_listing in CACHE_IMPLEMENTATIONS[0][1], (
            #     f'Cache method must be listed in {decorator.__module__}.py%s CACHE_IMPLEMENTATIONS '
            #     f'to avoid speghettification, \n (in DIRECT_SET)' % "'s"
            # )
            cache_key = get_cache_key(func, *args)
            result = cache.get(cache_key)
            if not result:
                result = func(*func_args, **func_kwargs)
                cache.set(cache_key, result)
            print(type(result))
            return result
        return wrapper_method
    return decorator


def get_cache_key(func, *args):
    possible_cache_keys = (
        'user',
        'group',
    )
    cache_key = f'{func.__module__}.{func.__qualname__}'
    if args:
        for key in args:
            if key in possible_cache_keys:
                # implement logic to get the cache key here
                pass
            else:
                raise NotImplementedError('get_cache_key does not support caching for %s key that '
                                          'you provided in the decorator\n Possible choices are:- \n '
                                          '%s' % key % possible_cache_keys)
    return cache_key


