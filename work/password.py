import hashlib
import math
import random

import numpy as np

from util.generator import generate_random_str


def password_hashing_and_checking_task(
    stored_hashes_count: int,
    tried_hashes_count: int,
    password_length_range: tuple[int, int],
    correct_hashes_ratio: float,
    work_index: int = 0,
) -> int:
    # Generate stored passwords
    stored_passwords = generate_passwords(stored_hashes_count, password_length_range)

    # Generate test passwords
    test_passwords = generate_test_passwords(
        stored_passwords,
        tried_hashes_count,
        password_length_range,
        correct_hashes_ratio,
    )

    # Generate stored hashes
    stored_hashes = {pwd: sha256_hash(pwd) for pwd in stored_passwords}

    hashes_matched = 0

    # Hash and check passwords
    for password in test_passwords:
        test_hash = sha256_hash(password)
        if test_hash in stored_hashes.values():
            hashes_matched += 1
            continue

    return hashes_matched


def generate_test_passwords(
    stored_passwords: list[str],
    test_count: int,
    password_length_range: tuple[int, int],
    correct_hashes_ratio: float,
) -> list[str]:
    correct_test_password_count = int(test_count * correct_hashes_ratio)
    incorrect_test_password_count = test_count - correct_test_password_count

    incorrect_test_passwords = generate_passwords(
        incorrect_test_password_count, password_length_range
    )

    stored_passwords_count = len(stored_passwords)

    correct_test_password_pool = stored_passwords
    if correct_test_password_count > stored_passwords_count:
        ratio = int(math.ceil(correct_test_password_count / stored_passwords_count))
        correct_test_password_pool = random.choices(
            stored_passwords, k=int(stored_passwords_count * ratio)
        )

    correct_test_passwords = random.sample(
        correct_test_password_pool, correct_test_password_count
    )
    test_passwords = correct_test_passwords + incorrect_test_passwords
    random.shuffle(test_passwords)

    return test_passwords


def generate_passwords(
    passwords_count: int, password_length_range: tuple[int, int]
) -> list[str]:
    """
    Generates a list of random passwords.

    Args:
        num_passwords (int): Number of passwords to generate.
        password_length_range (tuple): Range of password lengths (min, max).

    Returns:
        list: List of randomly generated passwords.
    """
    passwords: list[str] = []

    for _ in range(passwords_count):
        password_length = random.randint(*password_length_range)
        password = generate_random_str(password_length)

        passwords.append(password)

    return passwords


def sha256_hash(password: str) -> str:
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def password_hashing_and_checking_task_random_params() -> list:
    """
    Generates random parameters for the password hashing and checking task.

    Returns:
        list: Randomly generated parameters for the task.
    """
    # Generate random passwords
    stored_hashes_count = random.randint(1000, 10000)
    tried_hashes_count = random.randint(100, 1000)
    password_length_range = (random.randint(6, 20), random.randint(21, 30))
    correct_hashes_ratio = random.uniform(0.1, 0.9)

    return [
        stored_hashes_count,
        tried_hashes_count,
        password_length_range,
        correct_hashes_ratio,
    ]
