import random
from .basic_types import default


class Arbitrary(object):
    values_tree = None

    def some_of(self, iterable, empty=True):
        iter_len = len(iterable)
        start_from = 0
        if not empty:
            if iter_len == 1:
                return iterable
            elif iter_len == 0:
                raise ValueError('Iterable can not be empty')
        take_n = random.randint(start_from, iter_len)
        if not empty and take_n == start_from:
            take_n += 1
        return self.shuffle(iterable)[start_from:take_n]

    def one_of(self, *options):
        """
        >>> A().one_of(1)
        1
        >>> A().one_of(1, 2) in [1, 2]
        True
        """
        width = len(options)
        if width == 0:
            raise ValueError('Not enought options')
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
