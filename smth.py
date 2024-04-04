import time
from math import ceil
from functools import wraps


def outer(n, flag=False):
    def timer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            total = 0
            for _ in range(n):
                start = time.perf_counter()
                result = func(*args, **kwargs)
                end = time.perf_counter()
                total += end - start
            avg_time = total / n
            if flag:
                print(f"Avg Time: {avg_time}, total: {total}")
            print(total)
            return result
        return wrapper
    return timer



