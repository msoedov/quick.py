from unittest import TestCase
from quick.core import generate, A


class TestGenerate(TestCase):

    def test_generate_map(self):

        def foo(x: {str: int}):
            return x

        fn, kw = generate(foo)
        self.assertIsInstance(kw['x'], dict)
        self.assertIs(fn, foo)

    def test_generate_map_nested_gen(self):

        def int_gen(a: A):
            return 1

        def foo(x: {int_gen: str}):
            return x

        fn, kw = generate(foo)
        self.assertIsInstance(kw['x'], dict)
        self.assertIs(fn, foo)

        self.assertIsInstance(kw['x'][1], str)
