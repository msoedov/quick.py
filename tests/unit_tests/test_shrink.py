import unittest

from quick.features import QuickCheck, verify
from quick.generators import A, positive_num


def list_of(t: type, n):

    def seq(lst: [t]):
        return lst[:n]

    return seq


def assert_simpler(before, after):
    if before == after:
        return

    if not after:
        return

    for k, v in before.items():
        if k not in after:
            continue

        if isinstance(v, dict):
            assert_simpler(v, after[k])
            continue

        if v < after[k]:
            raise AssertionError("{} < {}".format(before, after))


class TestGen(unittest.TestCase):

    def setUp(self):
        self.qc = QuickCheck()

    def assertLenUpTo(self, seq, limit, msg=None):

        self.assertLessEqual(len(seq), limit, msg=msg)

    def assertInRange(self, val, low, hi):
        assert low <= val <= hi

    def test_shrink_int(self):
        """
        It should shrink value from 10 to 20
        """

        @self.qc.forall("Sample property that generally invalid")
        def prop(x: positive_num):
            return x < 10

        experiments = list(self.qc.experiments.values())

        self.assertEqual(len(experiments), 1)

        sample_experiment = experiments[0]

        args = verify(sample_experiment, simplification=True)
        ok, kwargs, shrunked, simplified_to = args
        self.assertEqual(ok, False)

        x = simplified_to["x"]
        self.assertInRange(x, 10, 20)
        assert_simpler(kwargs, simplified_to)

    def test_shrink_int_v2(self):

        @self.qc.forall("Sample property that generally invalid")
        def prop(x: positive_num):
            return 50 < x < 200

        experiments = list(self.qc.experiments.values())

        self.assertEqual(len(experiments), 1)

        sample_experiment = experiments[0]

        args = verify(sample_experiment, simplification=True)
        ok, kwargs, shrunked, simplified_to = args

        assert_simpler(kwargs, simplified_to)

    def test_shrink_list(self):
        """
        It should shrink list
        """

        @self.qc.forall("Sample property that generally invalid")
        def prop(x: list_of(positive_num, 10)):
            return len(x) == 4

        experiments = list(self.qc.experiments.values())

        self.assertEqual(len(experiments), 1)

        sample_experiment = experiments[0]

        args = verify(sample_experiment, simplification=True)
        ok, kwargs, shrunked, simplified_to = args

        self.assertEqual(ok, False)

        x = simplified_to["x"]
        self.assertLenUpTo(x, 5)
        assert_simpler(kwargs, simplified_to)

    def test_shrink_list_middle(self):
        """
        It should shrink list
        """

        def bit_seq(x: [bool], y: [bool]):
            return x + [1, 1, 1] + y

        @self.qc.forall("Sample property that generally invalid")
        def prop(x: bit_seq):
            return len(x) > 2 and all(map(lambda a: a == 1, x))

        experiments = list(self.qc.experiments.values())

        self.assertEqual(len(experiments), 1)

        sample_experiment = experiments[0]

        args = verify(sample_experiment, simplification=True)
        ok, kwargs, shrunked, simplified_to = args
        self.assertEqual(ok, False)
        self.assertEqual(shrunked, True)

        x = simplified_to["x"]
        self.assertLenUpTo(x, 5)
        self.assertIn(1, x)

    def test_shrink_dict(self):
        """
        It should shrink dict
        """

        def default(x):
            return x

        def key_str(x: default(str)):
            return x[:5]

        @self.qc.forall("Sample property that generally invalid")
        def prop(x: {key_str: positive_num}):
            x["a"] = 1
            return len(x) == 2

        experiments = list(self.qc.experiments.values())

        self.assertEqual(len(experiments), 1)

        sample_experiment = experiments[0]

        args = verify(sample_experiment, simplification=True)
        ok, kwargs, shrunked, simplified_to = args
        self.assertEqual(ok, False)
        self.assertEqual(shrunked, True)
        self.assertEqual(simplified_to, {"x": {}})
        assert_simpler(kwargs, simplified_to)

    def test_shrink_object(self):
        """
        It should shrink composition of generators
        """

        def email(name: str, host: str, domain: str):
            return "{}@{}.{}".format(name, host, domain)

        def user(username: str, mail: email):
            return dict(id=1, username=username[:7], mail=mail)

        @self.qc.forall("Sample property that generally invalid")
        def prop(u: user):
            return len(u["mail"]) < 20

        experiments = list(self.qc.experiments.values())

        self.assertEqual(len(experiments), 1)

        sample_experiment = experiments[0]

        args = verify(sample_experiment, simplification=True)
        ok, kwargs, shrunked, simplified_to = args

        assert_simpler(kwargs, simplified_to)


if __name__ == "__main__":
    unittest.main()
