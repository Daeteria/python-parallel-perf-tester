import datetime
import gc
import multiprocessing
import os
import random
import sys

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
    ):
        self.iterations = iterations
        self.task = task
        self.task_args = task_args
        self.task_count = task_count
        self.workers = workers
        self.wait_time_after_runner = wait_time_after_runner
        self.wait_time_after_iteration = wait_time_after_iteration
        self.gc_after_iteration = gc_after_iteration


def custom_task(name: str, func: callable, func_args: list) -> int:
    out = func(*func_args)
    return out


def test_pipeline(
    tasks: list[tuple[callable, list]],
    workers: list[int],
    iterations: int,
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

        job_details = "N/A"
        if len(tasks) > 0:
            job_details = "x".join([str(x) for x in tasks[0][1]])

        runners[key] = Runner(
            name=key, workers=num_workers, job_details=job_details, job_count=task_count
        )

    use_random_tasks = False
    if len(tasks) == 0:
        use_random_tasks = True

    for index in range(iterations):
        print(f"Test iteration {index+1}/{iterations}")
        print()

        # Initialize a set of random tasks
        if use_random_tasks:
            tasks = get_random_task_list(task_count=task_count)

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

    task_args = config.task_args

    if config.task == "sum":
        task_func = summing_task
    elif config.task == "multi":
        task_func = multiplication_task
    elif config.task == "io":
        task_func = io_task
    elif config.task == "zip":
        task_func = file_compression_task
    elif config.task == "tensor":
        task_func = tensor_task
    elif config.task == "sort":
        task_func = sorting_task
    elif config.task == "matrix":
        task_func = matrix_inversion_task
    elif config.task == "img":
        task_func = img_manipulation_task
        task_args = [cv2.imread("img.jpg")]
    elif config.task == "password":
        task_func = password_hashing_and_checking_task
    elif config.task == "random":
        task_func = None
    else:
        print("Invalid task specified. Quitting...")
        sys.exit(1)

    print(
        f"Starting test for task {config.task} with {config.task_count} tasks, {config.iterations} iterations"
    )

    if task_func is None:
        tasks = []
    else:
        tasks = get_task_list(
            task_count=config.task_count, task_func=task_func, task_args=task_args
        )

    runners = test_pipeline(
        tasks=tasks,
        workers=config.workers,
        iterations=config.iterations,
        task_count=config.task_count,
        wait_time_after_runner=config.wait_time_after_runner,
        wait_time_after_iteration=config.wait_time_after_iteration,
        gc_after_iteration=config.gc_after_iteration,
    )

    csv_data = []
    csv_data.append(
        [
            "Name",
            "Workers",
            "Job details",
            "Job count",
            "Time: init",
            "Time: work",
            "Time: task avg",
            "Time: total",
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


def get_random_task_list(task_count: int) -> list[tuple[callable, list]]:
    img = cv2.imread("img.jpg")
    tasks = [
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

    task_list = []
    for _ in range(task_count):
        random.seed(time.time())
        task_tuple = tasks[random.randint(0, len(tasks) - 1)]
        task_name = task_tuple[0]
        task_func = task_tuple[1]
        if task_name == "img":
            task_args = task_tuple[2]
        else:
            task_args = task_tuple[2]()

        task_list.append((task_func, task_args))

    return task_list


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
