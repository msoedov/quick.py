import unittest
from quick.features import QuickCheck, verify
from quick.generators import positive_num


class TestGen(unittest.TestCase):

    def setUp(self):
        self.qc = QuickCheck()

    def test_shrink_int(self):
        """
        It should shrink value from 10 to 20
        """

        @self.qc.forall('Sample property that generally invalid')
        def prop(x: positive_num):
            return x < 10

        experiments = list(self.qc.experiments.values())

        self.assertEqual(len(experiments), 1)

        sample_experiment = experiments[0]

        args = verify(sample_experiment, simplification=True)
        ok, kwargs, shrunked, simplified_to = args

        self.assertEqual(ok, False)

        self.assertIn(simplified_to['x'], range(10, 20))

    def test_shrink_int_v2(self):

        @self.qc.forall('Sample property that generally invalid')
        def prop(x: positive_num):
            return 100 < x < 200

        experiments = list(self.qc.experiments.values())

        self.assertEqual(len(experiments), 1)

        sample_experiment = experiments[0]

        args = verify(sample_experiment, simplification=True)
        ok, kwargs, shrunked, simplified_to = args

        self.assertEqual(ok, False)

        self.assertEqual(simplified_to['x'], 0)


if __name__ == '__main__':
    unittest.main()
