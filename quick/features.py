import sys
import unittest
from collections import namedtuple
from .core import generate
import concurrent.futures

config = {'max_count': 100, 'max_scale': sys.maxsize}
experiment = namedtuple('experiment', 'name fn config')

default = object()


class QuickCheck(object):

    def __init__(self, **settings):
        super(QuickCheck, self).__init__()
        self.settings = settings or config
        self.experiments = {}

    def __call__(self, experiment_name, **defaults):

        def decorator(fn):
            config = default
            if defaults:
                config = self.settings.copy()
                config.update(defaults)
            self.experiments[fn] = experiment(experiment_name, fn, config)
            return fn

        return decorator

    forall = __call__

    def run(self):
        for case in self.experiments.values():
            check(case, self.settings)

    def as_testcase(self, prototype=unittest.TestCase):

        class TestProperties(unittest.TestCase):
            """
            Automatically generated tests case based on quick check properties
            """

        settings = self.settings
        for experiment in self.experiments.values():
            if experiment.config is not default:
                settings = experiment.config
            max_count = settings['max_count']
            for x in range(max_count):

                def test_experiment(t):
                    test_case, input = generate(experiment.fn)
                    ok = test_case(**input)
                    t.assertTrue(ok, '`{}` Input: #{}'.format(experiment.name,
                                                              input))

                setattr(TestProperties, '{}#{}'.format(experiment.name, x),
                        test_experiment)
        return TestProperties


def check(experiment, settings):
    # todo: drop it
    print(experiment.name)
    if experiment.config is not default:
        settings = experiment.config
    max_count = settings['max_count']
    for x in range(max_count):
        test_case, input = generate(experiment.fn)
        ok = test_case(**input)
        if not ok:
            print('Fail %r' % input)
            break
        print('.', end='')
    print('')


forall = QuickCheck()
