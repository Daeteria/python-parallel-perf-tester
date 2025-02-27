import datetime
import os
import sys

from pipelines.handler import run_pipeline

from work_wrapper.task_parser import TaskWrapper
from util.config import load_runtime_config
from util.csv import csv_export
import argparse


def main():
    parser = argparse.ArgumentParser(description="Parallel Task Performance Tester")
    parser.add_argument("--config", type=str, help="Path to the configuration file")
    args = parser.parse_args()

    config = load_runtime_config(args.config)

    try:
        task_wrapper = TaskWrapper(config.task, config.task_args)
    except Exception as e:
        print(f"Failed to parse task: {e}. Quitting...")
        sys.exit(1)

    print(
        f"Starting test for task {config.task} with {config.task_count} tasks, {config.iterations} iterations"
    )

    runners = run_pipeline(
        task_func=task_wrapper.task_func,
        task_args=task_wrapper.task_args,
        workers=config.workers,
        iterations=config.iterations,
        task_count=config.task_count,
        task_details=task_wrapper.task_details,
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
            "Speedup (vs sequential)",
        ]
    )

    reference_tps = 0
    if "sequential" in runners:
        reference_tps = runners["sequential"].get_tasks_per_second()

    for key, runner in runners.items():
        csv_data.extend(runner.to_csv(reference_tps=reference_tps))

    csv_filename = f"results/{config.task}__{datetime.datetime.now().strftime('%Y_%m_%d__%H_%M')}.csv"

    os.makedirs("results", exist_ok=True)

    csv_export(data=csv_data, filename=csv_filename)

    print(f"Results saved to {csv_filename}")


if __name__ == "__main__":
    main()
