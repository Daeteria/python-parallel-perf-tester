import random
import numpy as np


def sorting_task(size: int, work_index: int = 0) -> np.ndarray:
    data = np.random.rand(size)
    return np.sort(data)


def sorting_task_random_params() -> list:
    size = random.randint(200000, 10000000)
    return [size]
