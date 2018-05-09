from quick.core import *


def property_basic(x: int):
    print(x)


def even_numbers(x: int):
    if x % 2:
        return x

    return x + 1


def property_custom_generators(x: even_numbers):
    print(x)


def property_vector(x: [int]):
    print(x)


def slice_gen(a: A):
    return a.slice_of(7, [int])


def property_vector(x: slice_gen):
    print(x)


def optional_bool(a: A):
    return a.one_of(True, None, False)


def age(a: A):
    return a.choose(18, 100)


def word(a: A):
    size = a.choose(4, 8)
    return a.slice_of(size, str)


def json_params(a: A):
    return {"age": age(a), "word": word(a)}


def email(a: A):
    return "{}@{}.{}".format(word(a), word(a), a.one_of("com", "net"))
