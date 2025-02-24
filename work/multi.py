import random


def multiplication_task(size: int, work_index: int = 0) -> float:
    out = 1
    for _ in range(size):
        out *= 1.00001
    return out


def multiplication_task_random_params() -> list:
    size = random.randint(10000, 10000000)
    return [size]
