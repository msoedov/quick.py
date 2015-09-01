import random
from .basic_types import random_for


class Arbitrary(object):
    values_tree = None

    def some_of(self, iterable, empty=True):
        pass

    def one_of(self, *options):
        width = len(options)
        index = random.randint(0, width - 1)
        return options[index]

    def slice_of(self, n, type=[int]):
        pass

    def choose(self, low, high, type=[int]):
        return random.randrange(low, high)

    def shuffle(self, *options):
        return random.shuffle(options)

    def default(self, t):
        return random_for(t)


A = Arbitrary
