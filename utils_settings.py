"""
Utility functions for Settings.
"""
import random
import string


def generate_random_name():
    """Generate a random name starting with 'D'."""
    name_length = random.randint(5, 10)  # Random length between 5 and 10
    random_chars = ''.join(random.choices(string.ascii_lowercase, k=name_length - 1))
    return 'D' + random_chars


def generate_random_username():
    """Generate a random username."""
    username_length = random.randint(8, 15)  # Random length between 8 and 15
    random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=username_length))
    return random_chars
