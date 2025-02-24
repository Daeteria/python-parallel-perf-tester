import gzip
import os
import random


def file_compression_task(filesize_mb: int, work_index: int):
    os.makedirs("tmp/compress", exist_ok=True)
    os.makedirs("tmp/decompress", exist_ok=True)

    filename = f"tmp/compress/random_file_{work_index}.bin"
    with open(filename, "wb") as f:
        f.write(os.urandom(filesize_mb * 1024 * 1024))

    compressed_filename = f"{filename}.gz"
    with open(filename, "rb") as f_in:
        with gzip.open(compressed_filename, "wb") as f_out:
            f_out.writelines(f_in)

    decompressed_filename = f"tmp/decompress/decompressed_file_{work_index}.bin"
    with gzip.open(compressed_filename, "rb") as f_in:
        with open(decompressed_filename, "wb") as f_out:
            f_out.write(f_in.read())

    os.remove(filename)
    os.remove(compressed_filename)
    os.remove(decompressed_filename)


def file_compression_task_random_params() -> list:
    filesize_mb = random.randint(1, 100)
    return [filesize_mb]
