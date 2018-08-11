import redis
from django.conf import settings


_redis_db = None


def get_redis():
    global _redis_db

    if _redis_db is None:
        redis_db = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB)
        _redis_db = redis_db
    else:
        redis_db = _redis_db

    return redis_db
