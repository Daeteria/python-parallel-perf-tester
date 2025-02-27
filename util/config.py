import json
import multiprocessing
import sys


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


def load_runtime_config(config_file: str) -> RuntimeConfig:

    if config_file is None:
        print("No configuration file specified. Quitting...")
        sys.exit(1)

    print(f"Using configuration file: {config_file}")

    config: RuntimeConfig = None

    try:
        with open(config_file, "r") as file:
            config_raw = json.load(file)
            config = RuntimeConfig(**config_raw)
    except Exception as e:
        print(f"Failed to read configuration file: {e}. Quitting...")
        sys.exit(1)

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

    return config
