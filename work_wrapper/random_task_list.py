import random
import time
import numpy as np

from work.img import img_manipulation_task
from work.io import io_task, io_task_random_params
from work.matrix import matrix_inversion_task, matrix_inversion_task_random_params
from work.multi import multiplication_task, multiplication_task_random_params
from work.password import (
    password_hashing_and_checking_task,
    password_hashing_and_checking_task_random_params,
)
from work.sort import sorting_task, sorting_task_random_params
from work.sum import summing_task, summing_task_random_params
from work.tensor import tensor_task, tensor_task_random_params
from work.zip import file_compression_task, file_compression_task_random_params


def get_random_task_list(
    task_count: int, task_types=list[str], img: np.ndarray = None
) -> list[tuple[callable, list]]:
    print(f"Generating a random task list of {task_count} tasks...")

    task_option_pool = [
        ("sum", summing_task, summing_task_random_params),
        ("multi", multiplication_task, multiplication_task_random_params),
        ("io", io_task, io_task_random_params),
        ("zip", file_compression_task, file_compression_task_random_params),
        ("tensor", tensor_task, tensor_task_random_params),
        ("sort", sorting_task, sorting_task_random_params),
        ("matrix", matrix_inversion_task, matrix_inversion_task_random_params),
        (
            "password",
            password_hashing_and_checking_task,
            password_hashing_and_checking_task_random_params,
        ),
        ("img", img_manipulation_task, [[img]]),
    ]

    task_options = []
    # If no task types are specified, use all available task types
    if len(task_types) == 0:
        task_options = task_option_pool
    else:
        # Limit options to specified task types
        for task_type in task_types:
            for option in task_option_pool:
                if task_type == option[0]:
                    task_options.append(option)

    print("Using task types: ", [opt[0] for opt in task_options])
    print()

    task_list = []
    for _ in range(task_count):
        random.seed(time.time())
        task_tuple = task_options[random.randint(0, len(task_options) - 1)]
        task_name = task_tuple[0]
        task_func = task_tuple[1]
        if task_name == "img":
            task_args = task_tuple[2].copy()
        else:
            task_args = task_tuple[2]()

        task_list.append((task_func, task_args))

    return task_list
