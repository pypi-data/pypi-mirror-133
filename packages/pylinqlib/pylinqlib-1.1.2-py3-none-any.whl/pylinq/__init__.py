import time
import typing
import numbers
import itertools

A = typing.TypeVar("A")
B = typing.TypeVar("B")
C = typing.TypeVar("C")


class pipe(typing.Generic[A, B]):
    def __init__(self, function: typing.Callable[[A], B]) -> None:
        self._function = function

    def __or__(self, a: A) -> B:
        return self._function(a)

    def __ror__(self, a: A) -> B:
        return self._function(a)


class depipe(typing.Generic[A, B, C]):
    def __init__(self, function: typing.Callable[[A, B], C]) -> None:
        self._function = function

    def __ror__(self, a: A) -> pipe[B, C]:
        return pipe(lambda x: self._function(a, x))


def dummy(x: typing.Any) -> typing.Any:
    return x


def compare(a: typing.Any, b: typing.Any) -> int:
    return 1 if a > b else -1 if a < b else 0


def equals(a: typing.Any, b: typing.Any) -> bool:
    return a == b


def empty() -> pipe[typing.Iterable[A], bool]:
    """
    Returns True if iterable is empty
    """

    def mapper(iterable: typing.Iterable[A]) -> bool:
        try:
            next(iter(iterable))
            return False
        except StopIteration:
            return True

    return pipe(mapper)


@typing.overload
def reduce(selector: typing.Callable[[A, A], A]) -> pipe[typing.Iterable[A], A]:
    """
    The lambda takes an accumulator (the first value from the list) and
    the current value as input.
    Returns the new value of the accumulator
    """


@typing.overload
def reduce(
    selector: typing.Callable[[B, A], B], initial: B
) -> pipe[typing.Iterable[A], B]:
    """
    The lambda takes an accumulator (second argument) and
    a current value as input.
    Returns the new value of the accumulator
    """


def reduce(selector, initial=None):
    if not initial:

        def mapper(iterable):
            iterator = iter(iterable)
            try:
                value = next(iterator)
            except StopIteration:
                raise ValueError("Iterable is empty")
            for i in iterator:
                value = selector(value, i)
            return value

    else:

        def mapper(iterable):
            nonlocal initial
            for i in iterable:
                initial = selector(initial, i)
            return initial

    return pipe(mapper)


def some(
    predicate: typing.Callable[[A], bool] = dummy
) -> pipe[typing.Iterable[A], bool]:
    """
    Returns True if at least one element
    satisfies the predicate
    """

    def mapper(iterable):
        for i in iterable:
            if predicate(i):
                return True
        return False

    return pipe(mapper)


def every(
    predicate: typing.Callable[[A], bool] = dummy
) -> pipe[typing.Iterable[A], bool]:
    """
    Returns True if all elements
    satisfies the predicate
    """

    def mapper(iterable):
        for i in iterable:
            if not predicate(i):
                return False
        return True

    return pipe(mapper)


@typing.overload
def average() -> pipe[typing.Iterable[numbers.Number], numbers.Number]:
    """
    Returns the average of an iterable of numbers
    """


@typing.overload
def average(
    selector: typing.Callable[[A], numbers.Number]
) -> pipe[typing.Iterable[A], numbers.Number]:
    """
    Returns the average of an iterable of numbers that
    obtained by applying a selector to each element
    """


def average(selector=dummy):
    def mapper(iterable):
        if iterable | empty():
            raise ValueError("Iterable is empty")
        result, size = 0, 0
        for i in iterable:
            result += selector(i)
            size += 1
        return result / size

    return pipe(mapper)


def chunk(size: int) -> pipe[typing.Iterable[A], typing.Iterable[typing.Iterable[A]]]:
    """
    Returns an iterable of iterables, each of which
    contains a maximum of `size` elements
    """

    def mapper(iterable):
        result = []
        buffer = []
        for i in iterable:
            buffer.append(i)
            if len(buffer) >= size:
                result.append(buffer.copy())
                buffer.clear()
        return result | concat() | buffer

    return pipe(mapper)


def concat() -> depipe[typing.Iterable[A], typing.Iterable[A], typing.Iterable[A]]:
    """
    Returns an iterable that contains items from both iterables
    """

    return depipe(lambda x, y: itertools.chain(x, y))


def contains(item: A) -> pipe[typing.Iterable[A], bool]:
    """
    Returns True if there is an item in the iterable,
    matching `item`
    """

    return pipe(some(item.__eq__).__ror__)


@typing.overload
def count() -> pipe[typing.Iterable[A], int]:
    """
    Returns the number of items in the iterable
    """


@typing.overload
def count(predicate: typing.Callable[[A], bool]) -> pipe[typing.Iterable[A], int]:
    """
    Returns the number of items in the iterable,
    satisfying the predicate
    """


def count(predicate=None):
    if predicate:
        return pipe(lambda x: sum(1 for i in x if predicate(i)))
    else:
        return pipe(lambda x: sum(1 for _ in x))


@typing.overload
def distinct() -> pipe[typing.Iterable[A], typing.Iterable[A]]:
    """
    Removes all the same elements while maintaining order
    """


@typing.overload
def distinct(
    comparer: typing.Callable[[A, A], bool]
) -> pipe[typing.Iterable[A], typing.Iterable[A]]:
    """
    Removes all identical elements using
    comparison functions `comparer`. Order is maintained
    """


def distinct(comparer=equals):
    def mapper(iterable):
        result = []
        iterable = list(iterable)
        while iterable:
            value = iterable.pop(0)
            result.append(value)
            for i in range(len(iterable) - 1, -1, -1):
                if comparer(value, iterable[i]):
                    del iterable[i]
        return result

    return pipe(mapper)


def at(index: int) -> pipe[typing.Iterable[A], A]:
    """
    Returns the element at index `index`.
    Invalid index will throw an error
    """

    def mapper(iterable):
        for i, v in enumerate(iterable):
            if i == index:
                return v
        raise ValueError("Index is out of range")

    return pipe(mapper)


@typing.overload
def difference() -> depipe[typing.Iterable[A], typing.Iterable[A], typing.Iterable[A]]:
    """
    Gets an iterable of items in iterables that are unique
    in relation to their own and other iterables
    """


@typing.overload
def difference(
    comparer: typing.Callable[[A, A], bool]
) -> depipe[typing.Iterable[A], typing.Iterable[A], typing.Iterable[A]]:
    """
    Returns an iterable of iterable items,
    which are unique in relation to their own and other iterables,
    using the compare function "comparer"
    """


def difference(comparer=equals):
    def mapper(iterable, other):
        elements = (
            iterable | distinct(comparer) | concat() | (other | distinct(comparer))
        )
        return (
            elements
            | distinct(comparer)
            | where(lambda x: (elements | count(lambda y: comparer(x, y))) == 1)
        )

    return depipe(mapper)


@typing.overload
def group_by(
    key_selector: typing.Callable[[A], B]
) -> pipe[typing.Iterable[A], dict[B, typing.Iterable[A]]]:
    """
    Groups an iterable by key. It is important to
    the key was hashable because a dictionary is being used
    """


@typing.overload
def group_by(
    key_selector: typing.Callable[[A], B], comparer: typing.Callable[[B, B], bool]
) -> pipe[typing.Iterable[A], typing.Iterable[typing.Tuple[B, typing.Iterable[A]]]]:
    """
    Groups an iterable by key. The dictionary is not used, so
    there are no key restrictions. Use with care as
    complexity is extremely high
    """


def group_by(key_selector, comparer=None):
    if not comparer:

        def mapper(iterable):
            result = {}
            for i in iterable:
                key = key_selector(i)
                if key in result:
                    result[key].append(i)
                else:
                    result[key] = [i]
            return result

    else:

        def mapper(iterable):
            result = []
            for i in iterable:
                key = key_selector(i)
                has = False
                for k, v in result:
                    if comparer(k, key):
                        v.append(i)
                        has = True
                        break
                if not has:
                    result.append((key, [i]))
            return result

    return pipe(mapper)


@typing.overload
def maximal() -> pipe[typing.Iterable[A], A]:
    """
    Returns the maximal element according to
    the standard function `compare`
    """


@typing.overload
def maximal(comparer: typing.Callable[[A, A], int]) -> pipe[typing.Iterable[A], A]:
    """
    Returns the maximal element according to
    comparison function `comparer`
    """


def maximal(comparer=compare):
    def mapper(iterable):
        if iterable | empty():
            raise ValueError("Iterable is empty")
        iterator = iter(iterable)
        current = next(iterator)
        for i in iterator:
            if comparer(i, current) == 1:
                current = i
        return current

    return pipe(mapper)


@typing.overload
def minimal() -> pipe[typing.Iterable[A], A]:
    """
    Returns the minimal element according to
    the standard function `compare`
    """


@typing.overload
def minimal(comparer: typing.Callable[[A, A], int]) -> pipe[typing.Iterable[A], A]:
    """
    Returns the minimal element according to
    comparison functions `comparer`
    """


def minimal(comparer=compare):
    def mapper(iterable):
        if iterable | empty():
            raise ValueError("Iterable is empty")
        iterator = iter(iterable)
        current = next(iterator)
        for i in iterator:
            if comparer(i, current) == -1:
                current = i
        return current

    return pipe(mapper)


def of_type(cls: typing.Type[A]) -> pipe[typing.Iterable, typing.Iterable[A]]:
    """
    Returns an iterable with only elements of the given type
    """

    return pipe(lambda x: filter(lambda y: isinstance(y, cls), x))


@typing.overload
def sort() -> pipe[typing.Iterable[A], A]:
    """
    Returns a sorted iterable according to
    the standard function `compare`
    """


@typing.overload
def sort(comparer: typing.Callable[[A, A], int]) -> pipe[typing.Iterable[A], A]:
    """
    Returns a sorted iterable according to
    comparison functions `comparer`
    """


def sort(comparer=compare):
    def mapper(iterable):
        def recursive(current):
            if len(current) < 2:
                return current
            pivot = current[int(len(current) / 2)]
            left_node, right_node = [], []
            for i in current:
                if comparer(i, pivot) == -1:
                    left_node.append(i)
                else:
                    right_node.append(i)
            return recursive(left_node) + recursive(right_node)

        return recursive(list(iterable))

    return pipe(mapper)


def select(
    selector: typing.Callable[[A], B]
) -> pipe[typing.Iterable[A], typing.Iterable[B]]:
    """
    Applies a transform function to each item
    """

    return pipe(lambda x: map(selector, x))


def skip(items: int) -> pipe[typing.Iterable[A], typing.Iterable[A]]:
    """
    Skips `count` items from the iterable. Negative
    index not allowed.
    """

    def mapper(iterable):
        iterator = iter(iterable)
        for _ in range(items):
            try:
                next(iterator)
            except StopIteration:
                return []
        return iterator

    assert items >= 0
    return pipe(mapper)


def skip_while(
    predicate: typing.Callable[[A], bool]
) -> pipe[typing.Iterable[A], typing.Iterable[A]]:
    """
    Excludes items from the resulting iterable until any
    the element will not satisfy the predicate
    """

    def mapper(iterable):
        iterator = iter(iterable)
        try:
            while True:
                value = next(iterator)
                if not predicate(value):
                    return itertools.chain([value], iterator)
        except StopIteration:
            return []

    return pipe(mapper)


def take(items: int) -> pipe[typing.Iterable[A], typing.Iterable[A]]:
    """
    Returns an iterable whose length is at most `count`.
    Negative index not allowed.
    """

    def mapper(iterable):
        iterator = iter(iterable)
        result = []
        try:
            for _ in range(items):
                result.append(next(iterator))
        finally:
            return result

    assert items >= 0
    return pipe(mapper)


def take_while(
    predicate: typing.Callable[[A], bool]
) -> pipe[typing.Iterable[A], typing.Iterable[A]]:
    """
    Adds items to the resulting iterable while items
    satisfy the predicate
    """

    def mapper(iterable):
        iterator = iter(iterable)
        result = []
        try:
            while True:
                value = next(iterator)
                if predicate(value):
                    result.append(value)
                else:
                    return result
        except StopIteration:
            return result

    return pipe(mapper)


def to_dict(
    key_selector: typing.Callable[[A], B],
    value_selector: typing.Callable[[A], C] = dummy,
) -> pipe[typing.Iterable[A], typing.Dict[B, C]]:
    """
    Converts the list to a dictionary. Unlike group_by,
    the value is not an array, but the last matching one
    turnkey value
    """

    def mapper(iterable):
        result = {}
        for i in iterable:
            result[key_selector(i)] = value_selector(i)
        return result

    return pipe(mapper)


def where(
    predicate: typing.Callable[[A], bool]
) -> pipe[typing.Iterable[A], typing.Iterable[A]]:
    """
    Returns an iterable where all elements satisfy a predicate
    """

    return pipe(lambda x: filter(predicate, x))


def collect(
    create: typing.Callable[[], B],
    append: typing.Callable[[B, A], B or None],
    new: typing.Callable[[B], C] = dummy,
    stateful: bool = False,
) -> pipe[typing.Iterable[A], C]:
    """
    Function for control all steps of
    collecting iterable. Set `stateful`
    to True if given object has its own
    state used to collect iterable
    """

    if not stateful:

        def mapper(iterable):
            result = create()
            for i in iterable:
                result = append(result, i)
            return new(result)

    else:

        def mapper(iterable):
            result = create()
            for i in iterable:
                append(result, i)
            return new(result)

    return pipe(mapper)
