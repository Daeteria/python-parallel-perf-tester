def get_task_list(
    task_count: int, task_func: callable, task_args: list
) -> list[tuple[callable, list]]:
    tasks = []
    for index in range(task_count):
        tasks.append((task_func, task_args))
    return tasks
