# quick.py

[![Join the chat at https://gitter.im/msoedov/quick.py](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/msoedov/quick.py?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

quick.py is property-based testing library for Python inspired by the Haskell library QuickCheck. The core idea of QuickCheck is that instead of enumerating expected input and output for unit tests, you write properties about your function that should hold true for all inputs. This lets you write concise, powerful tests.


Examples
-------

Basic example:

```python
# example.py
from quick.features import QuickCheck

qc = QuickCheck(max_count=100)


@qc.forall('Associative of addition for integers')
def prop(x: int, y: int):
    return (x + y) == (y + x)


TestAddtion = qc.as_testcase()

```

```shell
>>> nosetests example.py
....................................................................................................
----------------------------------------------------------------------
Ran 100 tests in 0.061s

OK

```


Custom generators:

```python
# example.py
from quick.features import QuickCheck
from quick.generators import number
from quick.arbitrary import A

qc = QuickCheck(max_count=100)


def non_empty_list(el: number, ls: [number]):
    """
    Generator which always returns non empty list
    """
    ls.append(el)
    return ls


@qc.forall('Sorted lists first element should be always lesser or eq than last')
def prop(x: non_empty_list):
    sorted_x = sorted(x)
    first = sorted_x[0]
    last = sorted_x[-1]
    return first <= last


TestSort = qc.as_testcase()

```

```shell
>>> nosetests example.py
....................................................................................................
----------------------------------------------------------------------
Ran 100 tests in 0.070s

OK

```


Features
--------
- Integration with unittests library
- Custom generators
- Simplification/Shrinking of failure input (in progress)

Controlled Randomness
---------------------

```python

def working_time(a: A):
    day = a.choose_one('Monday', 'Tuesday', 'Wednesday', 'Thursday')
    hour = a.choose(8, 17)
    return {'day': day, 'hour': hour}

```

Custom object generators
-----------------


```python
class User(object):

    def __init__(self, name, age):
        self.name = name
        self.age = age


def user_gen(name: str, a: A):
    age = a.choose(18, 100)
    return User(name, age)


forall('Valid users')
def prop(user: user_gen):
    return ...
```

Shrinking
---------

TBD




Python 2 support?
-----------------
Oups, sorry


Getting Help
------------

For **feature requests** and **bug reports** [submit an issue
](https://github.com/msoedov/quick/issues) to the GitHub issue tracker for
quick.py.

