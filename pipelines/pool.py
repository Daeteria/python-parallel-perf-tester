from dataclasses import dataclass
from multiprocessing import Pool
from typing import Any, Callable, Generic, TypeVar

from easy_pool.easy_pool import EasyPool
from util.math import avg_float
from util.timer import Timer

T = TypeVar("T")
R = TypeVar("R")


@dataclass
class IndexedTask(Generic[T, R]):
    index: int
    func: Callable[[T], R]
    args: T


def process_indexed_task(task: IndexedTask[Any, Any]) -> tuple[int, Any, float]:
    timer = Timer(start_now=True)
    result = task.func(*task.args)
    return (task.index, result, timer.get_duration())


def pool_test_pipeline(
    pool_size: int,
    tasks: list[tuple[callable, list]],
) -> tuple[float, float, float, float]:
    """
    Executes a test pipeline using a pool of workers to process tasks.
    Args:
        pool_size (int): The number of workers in the pool.
        tasks (list[tuple[callable, list]]): A list of tasks, where each task is represented
                                             as a tuple containing a callable and a list of arguments.
    Returns:
        A tuple of floats containing the following values:
        - The runtime for task creation.
        - The runtime for waiting for all tasks to complete.
        - The average runtime of each task.
        - The total runtime of the test.
    """

    print_prefix = f"Pool test pipeline: Pool size={pool_size} |"
    print(f"{print_prefix} Starting test...")
    timer = Timer(start_now=True)

    easy_pool = EasyPool(pool_size=pool_size)

    for index, task_tuple in enumerate(tasks):
        task_func, task_args = task_tuple
        task_args_with_index = task_args + [index]
        easy_pool.add_task(index, task_func, task_args_with_index)

    print(f"{print_prefix} Task creation runtime: {timer.get_duration_str()}")

    init_runtime = timer.get_duration()
    collect_timer = Timer(start_now=True)

    # Blocking until all tasks are done
    results = easy_pool.get_results()
    print(f"{print_prefix} Work (waiting) runtime: {collect_timer.get_duration_str()}")
    work_runtime = collect_timer.get_duration()

    avg_task_runtime = avg_float([runtime for _, _, runtime in results])

    del easy_pool

    print(f"{print_prefix} Total time: {timer.get_duration_str()}")
    print()

    total_runtime = timer.get_duration()

    return init_runtime, work_runtime, avg_task_runtime, total_runtime
