import os
import sys
import random

max_num = sys.maxsize
generation_width = 200


def random_for(primitive_type):
    if primitive_type == float:
        return random.uniform(-max_num, max_num)
    elif primitive_type == int:
        return random.randint(-max_num, max_num)
    elif primitive_type == str:
        return ''
    elif primitive_type == bytes:
        size = random.randint(0, generation_width)
        return bytes([random.randint(0, 255) for _ in range(size)])


def default(type,
            lo=-max_num,
            hi=max_num,
            complex_size=generation_width,
            min_complexity=0):
    if type == float:
        return random.uniform(lo, hi)
    elif type == int:
        return random.randint(lo, hi)
    elif type == str:
        return ''
    elif type == bytes:
        size = random.randint(min_complexity, complex_size)
        lo = 0 if lo < 0 else lo
        hi = 255 if hi > 255 else hi
        return bytes([random.randint(lo, hi) for _ in range(size)])
