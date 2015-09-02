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
        return bytes(random.randint(size))
