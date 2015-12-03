import unittest
from quick import Value, Values, A


def abc_generator(a: A):
    return a.some_of(['a', 'b', 'c'], empty=False)


def generator(x: int):
    return abs(x) % 10


class TestValues(unittest.TestCase):

    def test_value_abc(self):
        generated_value = Value(abc_generator)
        self.assertNotEqual(generated_value, [])
        for c in generated_value:
            self.assertIn(c, 'abc')
        self.assertLessEqual(len(generated_value), 3)

if __name__ == '__main__':
    unittest.main()
