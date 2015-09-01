"""
Quick check testing library for python
"""
import six
import abc
import os
import types
import random
import sys


from .features import cases
from .basic_types import random_for, generation_width
from .arbitrary import A

nil = None
numeric_types = [int, float]
seq_types = [str, bytes]
composable_types = (list, tuple, set, map, list)
basic_types = set(numeric_types + seq_types)

# todo: Decimal, Fraction

source = A()


def generate(annotated_property):
    annotations = annotated_property.__annotations__
    call_with = {}
    for val, _type in annotations.items():
        if isinstance(_type, types.FunctionType):
            gen, context = generate(_type)
            call_with[val] = gen(**context)
        elif _type.__hash__ and _type in basic_types:
            call_with[val] = random_for(_type)
        elif isinstance(_type, composable_types):
            if isinstance(_type, list):
                nested_type = _type[0]
                width = source.choose(0, generation_width)
                call_with[val] = list(
                    map(lambda pair: pair[0](**pair[1]), [generate(nested_type) for _ in range(width)]))
                continue
            raise NotImplementedError
        elif _type == A:
            call_with[val] = A()
        else:
            raise TypeError('Type to complex {}'.format(_type))
    return annotated_property, call_with


def quick_check():
    for case in cases.values():
        check(case)


def check(experiment):
    print(experiment.name)
    max_count = experiment.config['max_count']
    for x in range(max_count):
        test_case, input = generate(experiment.fn)
        ok = test_case(**input)
        if not ok:
            print('Fail %r' % values)
            break
        print('.', end='')
    print('')
