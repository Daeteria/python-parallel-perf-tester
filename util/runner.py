from util.math import avg_float_from_tuple_list


class Runner:
    def __init__(self, name: str, workers: int, task_details: str, task_count: int):
        self.name = name
        self.workers = workers
        self.runtimes = []
        self.task_details = task_details
        self.task_count = task_count

    def add_runtime(self, runtime: tuple[float, float, float, float]):
        self.runtimes.append(runtime)

    def get_avg_runtimes(self) -> tuple[float, float, float, float]:
        return avg_float_from_tuple_list(self.runtimes)

    def get_tasks_per_second(self) -> float:
        if len(self.runtimes) == 0:
            return 0

        avg_total_runtime = self.get_avg_runtimes()[3]
        if avg_total_runtime == 0:
            return 0

        return self.task_count / avg_total_runtime

    def to_csv(self) -> list[list]:
        return [
            [
                self.name,
                self.workers,
                self.task_details,
                self.task_count,
                *self.get_avg_runtimes(),
                self.get_tasks_per_second(),
            ]
        ]

    def print_runtimes(self):
        print(f"Runtime results for {self.name}:")

        avgs = self.get_avg_runtimes()
        print(f"AVG init: {round(avgs[0], 3)}")
        print(f"AVG work: {round(avgs[1], 3)}")
        print(f"AVG per task: {round(avgs[2], 3)}")
        print(f"AVG total: {round(avgs[3], 3)}")
        print()


def print_runtimes(runners: dict[str, Runner]):
    for _, runner in runners.items():
        runner.print_runtimes()
