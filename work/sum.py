import random


def summing_task(size: int, work_index: int = 0) -> int:
    out = 0
    for _ in range(size):
        out += 1
    return out


def summing_task_random_params() -> list:
    size = random.randint(10000, 10000000)
    return [size]
