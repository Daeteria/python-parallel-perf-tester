import gc
import sys
import time
from typing import Optional

import cv2

from pipelines.pool import pool_test_pipeline
from pipelines.sequential import sequential_test_pipeline
from util.runner import Runner, print_runtimes
from work_wrapper.random_task_list import get_random_task_list
from work_wrapper.task_list import get_task_list


def run_pipeline(
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

    img = cv2.imread("img.jpg")

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
            tasks = get_random_task_list(
                task_count=task_count, task_types=task_args, img=img
            )

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
