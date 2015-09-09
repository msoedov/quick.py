import random
from .basic_types import default


class Arbitrary(object):
    values_tree = None

    def some_of(self, iterable, empty=True):
        start_from = 0 if not empty else 1
        take_n = random.randint(start_from, len(iterable))
        return self.shuffle(iterable)[start_from:take_n]

    def one_of(self, *options):
        width = len(options)
        index = random.randint(0, width - 1)
        return options[index]

    def slice_of(self, n, iterable, empty=True):
        assert n < len(iterable)
        start_from = 0 if not empty else 1
        take_n = random.randint(start_from, n)
        # todo: improve
        return iterable[start_from:take_n]

    def choose(self, low, high, type=[int]):
        return random.randrange(low, high)

    def shuffle(self, options):
        random.shuffle(options)
        return options

    def default(self, t):
        return default(t)


A = Arbitrary
