import random


def generate_random_string(pattern, length):
    return ''.join(random.sample(pattern, length))
