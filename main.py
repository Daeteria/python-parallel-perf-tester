import datetime
import gc
import multiprocessing
import os
import random
import sys
from typing import Optional

import cv2
from pipelines.pool import pool_test_pipeline
from pipelines.sequential import sequential_test_pipeline

import time

from util.csv import csv_export
import argparse
import json
from util.runner import Runner, print_runtimes
from work.compression import file_compression_task, file_compression_task_random_params
from work.img import img_manipulation_task
from work.io import io_task, io_task_random_params
from work.math import (
    multiplication_task,
    multiplication_task_random_params,
    summing_task,
    summing_task_random_params,
)
from work.matrix_inv import matrix_inversion_task, matrix_inversion_task_random_params
from work.password import (
    password_hashing_and_checking_task,
    password_hashing_and_checking_task_random_params,
)
from work.sort import sorting_task, sorting_task_random_params
from work.tensor import tensor_task, tensor_task_random_params


class RuntimeConfig:
    def __init__(
        self,
        iterations: int,
        task: str,
        task_args: list,
        task_count: int,
        workers: list[int],
        wait_time_after_runner: float = None,
        wait_time_after_iteration: float = None,
        gc_after_iteration: bool = False,
        multiprocessing_start_method: str = None,
    ):
        self.iterations = iterations
        self.task = task
        self.task_args = task_args
        self.task_count = task_count
        self.workers = workers
        self.wait_time_after_runner = wait_time_after_runner
        self.wait_time_after_iteration = wait_time_after_iteration
        self.gc_after_iteration = gc_after_iteration
        self.multiprocessing_start_method = multiprocessing_start_method


def custom_task(name: str, func: callable, func_args: list) -> int:
    out = func(*func_args)
    return out


def test_pipeline(
    task_func: Optional[callable],
    task_args: list,
    workers: list[int],
    iterations: int,
    task_details: str,
    task_count: int = 0,
    wait_time_after_runner: float = None,
    wait_time_after_iteration: float = None,
    gc_after_iteration: bool = False,
) -> dict[str, Runner]:
    runners: dict[str, Runner] = {}
    for num_workers in workers:
        if num_workers != 0:
            key = f"parallel_{num_workers}"
        else:
            key = "sequential"

        runners[key] = Runner(
            name=key,
            workers=num_workers,
            task_details=task_details,
            task_count=task_count,
        )

    tasks: list[tuple[callable, list]] = []

    # Get tasks list for pipeline
    if task_func is not None:
        tasks = get_task_list(
            task_count=task_count, task_func=task_func, task_args=task_args
        )

    for index in range(iterations):
        print(f"Test iteration {index+1}/{iterations}")
        print()

        # Initialize a set of random tasks
        if task_func is None:
            tasks = get_random_task_list(task_count=task_count, task_types=task_args)

        # For whatever reason the tasks list is empty
        if len(tasks) == 0:
            print("No tasks specified to run pipelines with. Quitting...")
            sys.exit(1)

        # Run tests
        for key, runner in runners.items():
            print(f"Running test for {key}")
            if runner.workers == 0:
                runners[key].add_runtime(sequential_test_pipeline(tasks))
            else:
                runners[key].add_runtime(pool_test_pipeline(runner.workers, tasks))

            if wait_time_after_runner is not None:
                time.sleep(wait_time_after_runner)

        if gc_after_iteration:
            print("Running garbage collection...")
            print()
            gc.collect()

        if wait_time_after_iteration is not None:
            time.sleep(wait_time_after_iteration)

    print_runtimes(runners)
    return runners


def main():
    parser = argparse.ArgumentParser(description="Parallel Task Performance Tester")
    parser.add_argument("--config", type=str, help="Path to the configuration file")
    args = parser.parse_args()

    config_file = args.config

    if config_file is None:
        print("No configuration file specified. Quitting...")
        sys.exit(1)

    print(f"Using configuration file: {config_file}")

    config: RuntimeConfig = None

    with open(config_file, "r") as file:
        config_raw = json.load(file)
        config = RuntimeConfig(**config_raw)

    if config is None:
        print("Failed to load configuration. Quitting...")
        sys.exit(1)

    if config.wait_time_after_iteration is not None:
        if config.wait_time_after_iteration < 0:
            print("Invalid wait time after iteration: cannot be negative. Quitting...")
            sys.exit(1)

    if config.wait_time_after_runner is not None:
        if config.wait_time_after_runner < 0:
            print("Invalid wait time after runner: cannot be negative. Quitting...")
            sys.exit(1)

    if config.multiprocessing_start_method is not None:
        # Validate proposed start method
        if (
            config.multiprocessing_start_method
            not in multiprocessing.get_all_start_methods()
        ):
            print(
                f"Invalid multiprocessing start method: {config.multiprocessing_start_method}. Quitting..."
            )
            sys.exit(1)
        else:
            print(
                f"Using multiprocessing start method: {config.multiprocessing_start_method}"
            )
            multiprocessing.set_start_method(config.multiprocessing_start_method)

    task_args = config.task_args

    if config.task == "sum":
        task_func = summing_task
        task_details = "x".join([str(x) for x in task_args])
    elif config.task == "multi":
        task_func = multiplication_task
        task_details = "x".join([str(x) for x in task_args])
    elif config.task == "io":
        task_func = io_task
        task_details = "x".join([str(x) for x in task_args])
    elif config.task == "zip":
        task_func = file_compression_task
        task_details = "x".join([str(x) for x in task_args])
    elif config.task == "tensor":
        task_func = tensor_task
        task_details = "x".join([str(x) for x in task_args])
    elif config.task == "sort":
        task_func = sorting_task
        task_details = "x".join([str(x) for x in task_args])
    elif config.task == "matrix":
        task_func = matrix_inversion_task
        task_details = "x".join([str(x) for x in task_args])
    elif config.task == "img":
        task_func = img_manipulation_task
        img = cv2.imread("img.jpg")
        task_args = [img]
        task_details = f"{img.shape[0]}x{img.shape[1]}{img.shape[2]}"
    elif config.task == "password":
        task_func = password_hashing_and_checking_task
        task_details = f"{task_args[0]}/{task_args[1]}; {task_args[2]}; {task_args[3]}"
    elif config.task == "random":
        task_func = None
        if len(task_args) == 0:
            task_details = "any"
        else:
            task_details = ";".join([str(x) for x in task_args])
    else:
        print("Invalid task specified. Quitting...")
        sys.exit(1)

    print(
        f"Starting test for task {config.task} with {config.task_count} tasks, {config.iterations} iterations"
    )

    runners = test_pipeline(
        task_func=task_func,
        task_args=task_args,
        workers=config.workers,
        iterations=config.iterations,
        task_count=config.task_count,
        task_details=task_details,
        wait_time_after_runner=config.wait_time_after_runner,
        wait_time_after_iteration=config.wait_time_after_iteration,
        gc_after_iteration=config.gc_after_iteration,
    )

    csv_data = []
    csv_data.append(
        [
            "Name",
            "Workers",
            "Task details",
            "Task count",
            "Time: init",
            "Time: work",
            "Time: task avg",
            "Time: total",
            "Tasks per second",
        ]
    )
    for key, runner in runners.items():
        csv_data.extend(runner.to_csv())

    csv_filename = f"results/{config.task}__{datetime.datetime.now().strftime('%Y_%m_%d__%H_%M')}.csv"

    os.makedirs("results", exist_ok=True)

    csv_export(data=csv_data, filename=csv_filename)

    print(f"Results saved to {csv_filename}")


def get_task_list(
    task_count: int, task_func: callable, task_args: list
) -> list[tuple[callable, list]]:
    tasks = []
    for index in range(task_count):
        tasks.append((task_func, task_args))
    return tasks


def get_random_task_list(
    task_count: int, task_types=list[str]
) -> list[tuple[callable, list]]:
    print(f"Generating a random task list of {task_count} tasks...")

    img = cv2.imread("img.jpg")
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
        ("img", img_manipulation_task, [img]),
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


if __name__ == "__main__":
    main()
