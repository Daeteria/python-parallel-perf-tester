from util.math import avg_float_from_tuple_list


class Runner:
    def __init__(self, name: str, workers: int, job_details: str, job_count: int):
        self.name = name
        self.workers = workers
        self.runtimes = []
        self.job_details = job_details
        self.job_count = job_count

    def add_runtime(self, runtime: tuple[float, float, float, float]):
        self.runtimes.append(runtime)

    def get_avg_runtimes(self) -> tuple[float, float, float, float]:
        return avg_float_from_tuple_list(self.runtimes)

    def to_csv(self) -> list[list]:
        return [
            [
                self.name,
                self.workers,
                self.job_details,
                self.job_count,
                *self.get_avg_runtimes(),
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
