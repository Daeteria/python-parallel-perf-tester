import cv2
from work.img import img_manipulation_task
from work.io import io_task
from work.matrix import matrix_inversion_task
from work.multi import multiplication_task
from work.password import password_hashing_and_checking_task
from work.sort import sorting_task
from work.sum import summing_task
from work.tensor import tensor_task
from work.zip import file_compression_task


class TaskWrapper:
    task_func: callable
    task_args: list
    task_details: str

    def __init__(self, task: str, task_args: list):
        self.task_func, self.task_args, self.task_details = self.parse_task(
            task, task_args
        )

    def __str__(self):
        return f"{self.task_func.__name__}({self.task_details})"

    def parse_task(self, task: str, task_args: list) -> tuple[callable, list, str]:
        if task == "sum":
            task_func = summing_task
            task_details = "x".join([str(x) for x in task_args])

        elif task == "multi":
            task_func = multiplication_task
            task_details = "x".join([str(x) for x in task_args])

        elif task == "io":
            task_func = io_task
            task_details = "x".join([str(x) for x in task_args])

        elif task == "zip":
            task_func = file_compression_task
            task_details = "x".join([str(x) for x in task_args])

        elif task == "tensor":
            task_func = tensor_task
            task_details = "x".join([str(x) for x in task_args])

        elif task == "sort":
            task_func = sorting_task
            task_details = "x".join([str(x) for x in task_args])

        elif task == "matrix":
            task_func = matrix_inversion_task
            task_details = "x".join([str(x) for x in task_args])

        elif task == "img":
            task_func = img_manipulation_task
            imgs = []
            for img_path in task_args[0]:
                img = cv2.imread(img_path)
                imgs.append(img)

            task_details = ";".join([str(x) for x in task_args[0]])
            task_args[0] = imgs

        elif task == "password":
            task_func = password_hashing_and_checking_task
            task_details = (
                f"{task_args[0]}/{task_args[1]}; {task_args[2]}; {task_args[3]}"
            )

        elif task == "random":
            task_func = None
            if len(task_args) == 0:
                task_details = "any"
            else:
                task_details = ";".join([str(x) for x in task_args])

        else:
            raise (f"Invalid task '{task}' specified.")

        return task_func, task_args, task_details
