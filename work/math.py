import random


def summing_task(size: int, work_index: int = 0) -> int:
    out = 0
    for _ in range(size):
        out += 1
    return out


def multiplication_task(size: int, work_index: int = 0) -> float:
    out = 1
    for _ in range(size):
        out *= 1.00001
    return out


def summing_task_random_params() -> list:
    size = random.randint(10000, 10000000)
    return [size]


def multiplication_task_random_params() -> list:
    size = random.randint(10000, 10000000)
    return [size]
