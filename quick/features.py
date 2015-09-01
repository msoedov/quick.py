def paralel(state=None):
    raise NotImplementedError


def nasty_strings():
    pass

import sys
from collections import namedtuple
from .core import generate


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

default = object()


class QuickCheck(object):

    def __init__(self, **settings):
        super(QuickCheck, self).__init__()
        self.settings = settings or config
        self.experiments = {}

    def __call__(self, experiment_name, **defaults):
        def decorator(fn):
            def wrapped(*args, **kwargs):
                return fn(*args, **kwargs)
            wrapped.__annotations__ = fn.__annotations__
            config = default
            if defaults:
                config = self.settings.copy()
                config.update(defaults)
            self.experiments[fn] = experiment(experiment_name, fn, config)
            return wrapped
        return decorator

    forall = __call__

    def run(self):
        for case in self.experiments.values():
            self.check(case)

    def check(self, experiment):
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
