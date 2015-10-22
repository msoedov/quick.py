import sys
import unittest
import functools
from copy import deepcopy
from collections import namedtuple
from .core import generate, flatten, Schema
from .shrink import shrink

config = {'max_count': 100, 'max_scale': sys.maxsize}
experiment = namedtuple('experiment', 'name fn config')

default = object()

debug = print


def verify(prop: experiment, simplification=False):
    test_case, schema = generate(prop.fn)
    kwargs = flatten(schema)
    ok = test_case(**kwargs)
    if ok:
        return True, kwargs, None, None
    if simplification:
        shrunked, simplified_to = shrink(test_case, schema)
    else:
        shrunked = False
        simplified_to = kwargs
    return False, kwargs, shrunked, simplified_to


def code_gen(experiment, x, skip_group, simplification=False):

    @skip_group
    def test_experiment(t):
        ok, kwargs, shrunked, simplified_to = verify(experiment, simplification)
        if not ok:
            description = '`{}` Input: #{}'.format(experiment.name, kwargs)
            if shrunked:
                description = '{}\nSimplified to: {}'.format(
                    description, simplified_to)
            else:
                description = '{}\n Failed to simplify'.format(description)
            t.assertTrue(ok, description)

    test_experiment.__doc__ = experiment.name
    return test_experiment


class QuickCheck(object):

    def __init__(self, **settings):
        super(QuickCheck, self).__init__()
        self.settings = settings or config
        self.experiments = {}

    def __call__(self, experiment_name, **defaults):

        def decorator(fn):
            config = default
            if defaults:
                config = deepcopy(self.settings)
                config.update(defaults)
            debug('Register {} to {}'.format(experiment_name, fn))
            self.experiments[experiment_name] = experiment(experiment_name, fn,
                                                           config)
            return fn

        return decorator

    forall = __call__

    def as_testcase(self,
                    prototype=unittest.TestCase,
                    skip_on_failure=True,
                    simplification=True):
        """
        :param prototype: class of test case
        :param skip_on_failure: boolean flag to skip all test group on first failure
        :return: test case class
        """
        debug('_' * 50)

        class TestProperties(prototype):
            """
            Automatically generated tests case based on quick check properties
            """

            @classmethod
            def should_fail(cls):
                cls.__unittest_expecting_failure__ = True
                return cls

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
        properties = []
        for experiment in self.experiments.values():
            if experiment.config is not default:
                settings = experiment.config
            max_count = settings['max_count']

            skip_group = skip_if()
            debug('Generating {} tests for [{}]'.format(max_count,
                                                        experiment.name))
            for x in range(max_count):
                test_experiment = code_gen(experiment, x, skip_group,
                                           simplification)
                setattr(TestProperties, '{}#{}'.format(experiment.name, x),
                        test_experiment)
                properties.append(test_experiment)
        TestProperties.properties = properties
        return TestProperties

    def verify(self):
        test_cls = self.as_testcase()
        test = test_cls()
        return [prop(test) for prop in test.properties]


forall = QuickCheck()
