import os
import random


def io_task(filesize_mb: int, work_index: int):

    os.makedirs("tmp/write", exist_ok=True)
    os.makedirs("tmp/copy", exist_ok=True)

    filename = f"tmp/write/random_file_{work_index}.bin"
    with open(filename, "wb") as f:
        f.write(os.urandom(filesize_mb * 1024 * 1024))

    copy_filename = f"tmp/copy/copy_file_{work_index}.bin"
    with open(filename, "rb") as f:
        with open(copy_filename, "wb") as f_copy:
            f_copy.write(f.read())

    os.remove(filename)
    os.remove(copy_filename)


def io_task_random_params() -> list:
    filesize_mb = random.randint(1, 100)
    return [filesize_mb]
