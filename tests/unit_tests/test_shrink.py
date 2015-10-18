import unittest
from quick.features import QuickCheck, verify


class TestGen(unittest.TestCase):

    def setUp(self):
        self.qc = QuickCheck()

    def test_shrink_int(self):

        @self.qc.forall('Sample property')
        def prop(x: int):
            return abs(x) < 10

        experiments = list(self.qc.experiments.values())

        self.assertEqual(len(experiments), 1)

        sample_experiment = experiments[0]

        args = verify(sample_experiment, simplification=True)
        ok, kwargs, shrunked, simplified_to = args

        self.assertEqual(ok, False)

        self.assertEqual(simplified_to['x'], 10)

    def test_shrink_int_v2(self):

        @self.qc.forall('Sample property')
        def prop(x: int):
            return 100 < abs(x) < 200

        experiments = list(self.qc.experiments.values())

        self.assertEqual(len(experiments), 1)

        sample_experiment = experiments[0]

        args = verify(sample_experiment, simplification=True)
        ok, kwargs, shrunked, simplified_to = args

        self.assertEqual(ok, False)

        self.assertEqual(simplified_to['x'], 10)


if __name__ == '__main__':
    unittest.main()
