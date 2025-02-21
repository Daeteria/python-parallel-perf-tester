import math
import random
import numpy as np


def tensor_task(size: int, tensor_count: int, work_index: int = 0) -> np.ndarray:
    a = get_tensor(size)

    if tensor_count <= 1:
        return a

    for _ in range(tensor_count - 1):
        b = get_tensor(size)
        a = np.dot(a, b)

    return a


def get_tensor(size: int):
    return np.random.rand(size, size)


def tensor_multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.tensordot(a, b)


def tensor_task_random_params() -> list:
    min_size, max_size = 128, 1024
    tensor_size = random.randint(min_size, max_size)

    # Logarithmic scaling for max tensor count
    min_count, max_count = 2, 12

    # Calculate scaling factor (logarithmic interpolation)
    scale = (math.log(tensor_size) - math.log(min_size)) / (
        math.log(max_size) - math.log(min_size)
    )
    max_tensor_count = int(round(min_count + (max_count - min_count) * (1 - scale)))

    # Generate a random tensor count between 2 and max_tensor_count
    tensor_count = random.randint(2, max_tensor_count)

    return [tensor_size, tensor_count]
