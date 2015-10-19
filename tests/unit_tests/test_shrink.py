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

        self.assertEqual(simplified_to['x'], 100)

    def test_shrink_list(self):
        """
        It should shrink list
        """

        @self.qc.forall('Sample property that generally invalid')
        def prop(x: [positive_num]):
            return len(x) <= 4

        experiments = list(self.qc.experiments.values())

        self.assertEqual(len(experiments), 1)

        sample_experiment = experiments[0]

        args = verify(sample_experiment, simplification=True)
        ok, kwargs, shrunked, simplified_to = args

        self.assertEqual(ok, False)

        self.assertIn(len(simplified_to['x']), range(5, 10))

    def test_shrink_list_middle(self):
        """
        It should shrink list
        """

        def bit_seq(x: [bool], y: [bool]):
            return x + [1, 1, 1] + y

        @self.qc.forall('Sample property that generally invalid')
        def prop(x: bit_seq):
            return len(x) > 2 and all(map(lambda a: a == 1, x))

        experiments = list(self.qc.experiments.values())

        self.assertEqual(len(experiments), 1)

        sample_experiment = experiments[0]

        args = verify(sample_experiment, simplification=True)
        ok, kwargs, shrunked, simplified_to = args
        self.assertEqual(ok, False)
        self.assertEqual(shrunked, True)
        self.assertEqual(simplified_to['x'], [None, 1, 1,])

    def test_shrink_dict(self):
        """
        It should shrink dict
        """

        @self.qc.forall('Sample property that generally invalid')
        def prop(x: {str: positive_num}):
            x['a'] = 1
            return len(x) == 2

        experiments = list(self.qc.experiments.values())

        self.assertEqual(len(experiments), 1)

        sample_experiment = experiments[0]

        args = verify(sample_experiment, simplification=True)
        ok, kwargs, shrunked, simplified_to = args

        self.assertEqual(ok, False)
        self.assertEqual(shrunked, True)
        self.assertEqual(simplified_to['x'], {'a': 1})

    def test_shrink_object(self):
        """
        It should shrink composition of generators
        """
        @self.qc.forall('Sample property that generally invalid')
        def prop(x: {str: positive_num}):
            x['a'] = 1
            return len(x) == 2

        experiments = list(self.qc.experiments.values())

        self.assertEqual(len(experiments), 1)

        sample_experiment = experiments[0]

        args = verify(sample_experiment, simplification=True)
        ok, kwargs, shrunked, simplified_to = args

        self.assertEqual(ok, False)
        self.assertEqual(shrunked, True)
        self.assertEqual(simplified_to['x'], {'a': 1})


if __name__ == '__main__':
    unittest.main()
