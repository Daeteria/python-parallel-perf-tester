from util.timer import Timer


def sequential_test_pipeline(
    tasks: list[tuple[callable, list]]
) -> tuple[float, float, float, float]:
    """
    Executes a test pipeline processing tasks sequentially.
    Args:
        tasks (list[tuple[callable, list]]): A list of tasks, where each task is represented
                                             as a tuple containing a callable and a list of arguments.
    Returns:
        A tuple of floats containing the following values:
        - The runtime for task creation.
        - The runtime for waiting for all tasks to complete.
        - The average runtime of each task.
        - The total runtime of the test.
    """
    print(f"Sequential test pipeline: Starting test...")
    timer = Timer(start_now=True)

    for index, task_tuple in enumerate(tasks):
        task_func, task_args = task_tuple
        task_args_with_index = task_args + [index]
        res = task_func(*task_args_with_index)

    total_runtime = timer.get_duration()
    avg_task_runtime = total_runtime / len(tasks)

    print(f"Sequential test pipeline: Work runtime: {timer.get_duration_str()}")
    print()

    return (0, total_runtime, avg_task_runtime, total_runtime)
