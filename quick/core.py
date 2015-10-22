"""
Quick check testing library for python
"""
import types
from .basic_types import generation_width, default
from .arbitrary import A
from collections import namedtuple

nil = None
numeric_types = [int, float]
seq_types = [str, bytes]
composable_types = (list, tuple, set, dict)
basic_types = set(numeric_types + seq_types)

# todo: Decimal, Fraction

source = A()


class GenValue(namedtuple('GenValue', 'gen, kwargs')):

    def __hash__(self):
        """
        To make GenValue(lambda: None, {}) hashable
        """
        return hash(self.gen)

    def bind(self, fn):
        return


class Schema(dict):

    def __repr__(self):
        return 'Schema{}'.format(dict(self))


def reflect(val):
    if isinstance(val, types.FunctionType):
        fn, kw = generate(val)
        return GenValue(fn, kw)
    elif val in composable_types:
        return type_switch(val)
    return default(val)


def type_switch(t_var):
    if isinstance(t_var, list):
        nested_type = t_var[0]
        width = source.choose(0, generation_width)
        return [reflect(nested_type) for _ in range(width)]
    elif isinstance(t_var, dict):
        key_type, values_type = [e for e in t_var.items()][0]
        width = source.choose(0, generation_width)
        return {reflect(key_type): reflect(values_type) for _ in range(width)}
    elif isinstance(t_var, set):
        val_type = list(t_var)[0]
        width = source.choose(0, generation_width)
        return {reflect(val_type) for _ in range(width)}
    elif isinstance(t_var, tuple):
        return tuple(map(reflect, t_var))
    else:
        raise NotImplementedError


def flatten(node):
    """
    >>> flatten({'a': GenValue(lambda x: x+1, {'x': 1})})
    {'a': 2}
    >>> flatten({'a': GenValue(lambda x: x+1, {'x': GenValue(lambda c: c, {'c': 1})})})
    {'a': 2}
    """
    if isinstance(node, GenValue):
        fn, kw = node
        return fn(**flatten(kw))
    if isinstance(node, tuple):
        return tuple(flatten(v) for v in node)
    elif isinstance(node, dict):
        return {flatten(k): flatten(v) for k, v in node.items()}
    elif isinstance(node, list):
        return [flatten(v) for v in node]
    return node


def generate(annotated_property):
    """
    """
    if not hasattr(
            annotated_property,
            '__annotations__') or not annotated_property.__annotations__:
        raise AssertionError('{} no annotation?'.format(annotated_property))
    annotations = annotated_property.__annotations__
    call_with = Schema()
    for val, _type in annotations.items():
        if isinstance(_type, types.FunctionType):
            gen, context = generate(_type)
            call_with[val] = GenValue(gen, context)
        elif _type.__hash__ and _type in basic_types:
            call_with[val] = default(_type)
        elif isinstance(_type, composable_types):
            call_with[val] = type_switch(_type)
        elif _type == A:
            call_with[val] = A()
        else:
            raise TypeError('Type to complex {}'.format(_type))
    return annotated_property, call_with
