import sys
import unittest
import functools
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

    def as_testcase(self, prototype=unittest.TestCase, skip_on_failure=True):
        """
        :param prototype: class of test case
        :param skip_on_failure: boolean flag to skip all test group on first failure
        :return: test case class
        """

        class TestProperties(prototype):
            """
            Automatically generated tests case based on quick check properties
            """

        def skip_if():

            skip = False

            def wrap(fn):

                @functools.wraps(fn)
                def inner(*args, **kwargs):
                    nonlocal skip
                    if skip and skip_on_failure:
                        raise unittest.SkipTest('Failed experiment')
                    try:
                        return fn(*args, **kwargs)
                    except Exception as e:
                        skip = True
                        raise e

                return inner

            return wrap

        settings = self.settings
        for experiment in self.experiments.values():
            if experiment.config is not default:
                settings = experiment.config
            max_count = settings['max_count']

            skip_group = skip_if()
            for x in range(max_count):

                @skip_group
                def test_experiment(t):
                    test_case, input = generate(experiment.fn)
                    ok = test_case(**input)
                    t.assertTrue(ok, '`{}` Input: #{}'.format(experiment.name,
                                                              input))

                setattr(TestProperties, '{}#{}'.format(experiment.name, x),
                        test_experiment)
        return TestProperties


forall = QuickCheck()
