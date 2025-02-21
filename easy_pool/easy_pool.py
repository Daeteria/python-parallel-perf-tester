from dataclasses import dataclass
from multiprocessing import Pool
from multiprocessing.pool import AsyncResult
from typing import Any, Callable, Generic, TypeVar

from util.timer import Timer


T = TypeVar("T")
R = TypeVar("R")


@dataclass
class IndexedTask(Generic[T, R]):
    """
    A dataclass representing a generalized, indexed task that EasyPool can execute.
    """

    index: int
    func: Callable[[T], R]
    args: T


class EasyPool:
    """
    A simple wrapper around Python's multiprocessing.Pool to make it easy to run any arbitrary function in parallel.

    Add tasks to the pool using the add_task method, which calls the pool's apply_async method.
    After adding all tasks, call the get_results method to retrieve the results.
    This method will block until all tasks are done, or they timeout.

    The returned list is sorted by the index of each task.

    Args:
        pool_size (int): The number of workers in the pool.
        timeout (float, optional): The maximum time to wait for a result from a worker.

    Returns:
        list: A list of tuples containing the index, result, and runtime of each task.
    """

    def __init__(self, pool_size: int, timeout: float = None):
        self.pool_size = pool_size
        self.timeout = timeout
        self.pool = Pool(processes=pool_size)
        self.async_results: list[AsyncResult] = []

    @staticmethod
    def process_indexed_task(task: IndexedTask[Any, Any]) -> tuple[int, Any, float]:
        timer = Timer(start_now=True)
        result = task.func(*task.args)
        return (task.index, result, timer.get_duration())

    def add_task(self, task_index: int, task_func: Callable, task_args: list) -> Any:
        task = IndexedTask(task_index, task_func, task_args)
        self.async_results.append(
            self.pool.apply_async(self.process_indexed_task, (task,))
        )

    def get_results(self) -> list[tuple[int, Any, float]]:
        results = []
        for async_result in self.async_results:
            index, value, runtime = async_result.get(self.timeout)
            results.append((index, value, runtime))

        results.sort(key=lambda x: x[0])

        self.async_results = []
        return results

    def shutdown(self):
        if hasattr(self, "pool") is False or self.pool is None:
            return

        self.pool.terminate()
        del self.pool

    def __del__(self):
        self.shutdown()
