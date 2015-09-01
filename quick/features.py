def paralel(state=None):
    raise NotImplementedError


def nasty_strings():
    pass

import sys
from collections import namedtuple


config = {'max_count': 10, 'max_scale': sys.maxsize}
experiment = namedtuple('QuickCheckTest', 'name fn config')

cases = {}


def forall(name='', **defaults):
    def wrap(fn):
        def inn(*args, **kwargs):
            return fn(*args, **kwargs)
        inn.__annotations__ = fn.__annotations__
        conf = config.copy()
        conf.update(defaults)
        cases[fn] = experiment(name, fn, conf)
        return inn
    return wrap
