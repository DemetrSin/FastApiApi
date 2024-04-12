from functools import wraps


def decorator(func):
    def wrapper(*args, **kwargs):
        if args:
            yield func(*args)
        return func(**kwargs)

    return wrapper


@decorator
def foo(*args, **kwargs):
    lst = []
    if args:
        lst.append(sum(args))
        return lst
    return kwargs


print(next(foo(1, 2, 3))[0])
print(foo(a=1, b=2))


