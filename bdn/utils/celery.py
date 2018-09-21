import functools
from django.core.cache import cache


def single_instance_task(timeout):
    def task_exc(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            lock_id = 'celery-single-instance-{}-{}-{}'.format(
                func.__name__,
                ''.join(map(str, args)),
                ''.join(map(str, kwargs.values())))
            acquire_lock = lambda: cache.add(lock_id, 'true', timeout)  # noqa
            release_lock = lambda: cache.delete(lock_id)  # noqa
            if acquire_lock():
                try:
                    func(*args, **kwargs)
                finally:
                    release_lock()
        return wrapper
    return task_exc
