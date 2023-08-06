from functools import lru_cache
from math import factorial


@lru_cache
def tetrate(a, b):
    if not (b <= 2 or a * b < 10):
        raise MemoryError('Value too large to compute')
    if b == 0:
        return 1
    return a ** tetrate(a, b - 1)


@lru_cache
def double_factorial(a: int):
    if a < 0:
        raise ValueError('Argument to double factorial must be a positive integer')
    if a == 0 or a == 1:
        return 1
    return a * double_factorial(a - 2)


@lru_cache
def superfactorial(a: int):
    if a < 0:
        raise ValueError('Argument to superfactorial must be a positive integer')
    if a == 0:
        return 1
    return factorial(a) * superfactorial(a - 1)

@lru_cache
def hyperfactorial(a: int):
    if a < 0:
        raise ValueError('Argument to hyperfactorial must be a positive integer')
    if a == 0:
        return 1
    return (a ** a) * hyperfactorial(a - 1)

### FUTURE FEATURES ###

# def series(start: int, end: int, function):
#     pass
