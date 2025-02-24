import random
import numpy as np


def matrix_inversion_task(size: int, work_index: int = 0) -> np.ndarray:
    matrix = np.random.rand(size, size)
    return np.linalg.inv(matrix)


def matrix_inversion_task_random_params() -> list:
    size = random.randint(100, 2000)
    return [size]
