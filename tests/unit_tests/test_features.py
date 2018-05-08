import unittest

from quick.features import QuickCheck


class TestGen(unittest.TestCase):

    def setUp(self):
        self.qc = QuickCheck()

    def test_collector(self):
        matrix = {}

        @self.qc.forall('First property')
        def prop(x: int):
            matrix['first'] = True
            return True

        @self.qc.forall('Second property')
        def prop(x: int):
            matrix['second'] = True
            return True

        self.assertEqual(len(self.qc.experiments), 2)

        self.qc.verify()

        self.assertEqual(matrix, {'first': True, 'second': True})


if __name__ == '__main__':
    unittest.main()
