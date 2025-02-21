import datetime
import time


class Timer:
    def __init__(self, start_now=False):
        self.start_time = None

        if start_now:
            self.start()

    def start(self):
        self.start_time = time.time()

    def get_duration(self) -> float:
        return time.time() - self.start_time

    def get_duration_str(self) -> str:
        return str(datetime.timedelta(seconds=self.get_duration()))
