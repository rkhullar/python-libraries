import functools
import time
import datetime as dt


def timed(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        t1 = time.perf_counter()
        result = fn(*args, **kwargs)
        t2 = time.perf_counter()
        benchmark = dt.timedelta(seconds=t2-t1)
        print(f'completed in {benchmark}')
        return result
    return wrapper
