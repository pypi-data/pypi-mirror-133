"""Generic utility functions."""

import bisect
import copy
import functools
import importlib
import itertools
import typing
import warnings

from mutwo.utilities import constants


__all__ = (
    "scale",
    "scale_sequence_to_sum",
    "accumulate_from_n",
    "accumulate_from_zero",
    "insert_next_to",
    "uniqify_iterable",
    "cyclic_permutations",
    # "import_module_if_dependencies_have_been_installed",  # not for public use
    "find_closest_index",
    "find_closest_item",
    # "class_name_to_object_name",  # not for public use
    "get_nested_item_from_indices",
    "set_nested_item_from_indices",
    "find_numbers_which_sums_up_to",
    # call_function_except_attribute_error  # not for public use
)


def scale(
    value: constants.Real,
    old_min: constants.Real,
    old_max: constants.Real,
    new_min: constants.Real,
    new_max: constants.Real,
) -> constants.Real:
    """Scale a value from one range to another range.

    :param value: The value that shall be scaled.
    :param old_min: The minima of the old range.
    :param old_max: The maxima of the old range.
    :param new_min: The minima of the new range.
    :param new_max: The maxima of the new range.

    **Example:**

    >>> from mutwo.utilities import tools
    >>> tools.scale(1, 0, 1, 0, 100)
    100
    >>> tools.scale(0.5, 0, 1, 0, 100)
    50
    >>> tools.scale(0.2, 0, 1, 0, 100)
    20
    """

    try:
        assert old_min <= value <= old_max
    except AssertionError:
        message = (
            f"Input value '{value}' has to be in the range of (old_min = {old_min},"
            f" old_max = {old_max})."
        )
        raise ValueError(message)
    return (((value - old_min) / (old_max - old_min)) * (new_max - new_min)) + new_min


def scale_sequence_to_sum(
    sequence_to_scale: typing.Sequence[constants.Real], sum_to_scale_to: constants.Real
) -> typing.Sequence[constants.Real]:
    """Scale numbers in a sequence so that the resulting sum fits to the given value.

    :param sequence_to_scale: The sequence filled with real numbers which sum should fit
        to the given `sum_to_scale_to` argument.
    :type sequence_to_scale: typing.Sequence[constants.Real]
    :param sum_to_scale_to: The resulting sum of the sequence.
    :type sum_to_scale_to: constants.Real

    **Example:**

    >>> from mutwo import utilities
    >>> sequence_to_scale = [1, 3, 2]
    >>> utilities.tools.scale_sequence_to_sum(sequence_to_scale, 3)
    [0.5, 1.5, 1]
    """

    if sequence_to_scale:
        current_sum = sum(sequence_to_scale)
        if current_sum:
            factor = sum_to_scale_to / current_sum
            scaled_sequence = map(lambda number: number * factor, sequence_to_scale)
        else:
            n_items_to_scale = len(sequence_to_scale)
            size_per_item = sum_to_scale_to / n_items_to_scale
            scaled_sequence = (size_per_item for _ in sequence_to_scale)
        return type(sequence_to_scale)(scaled_sequence)
    else:
        return copy.copy(sequence_to_scale)


def accumulate_from_n(
    iterable: typing.Iterable[constants.Real], n: constants.Real
) -> typing.Iterator:
    """Accumulates iterable starting with value n.

    :param iterable: The iterable which values shall be accumulated.
    :param n: The start number from which shall be accumulated.

    **Example:**

    >>> from mutwo.utilities import tools
    >>> tools.accumulate_from_n((4, 2, 3), 0)
    (0, 4, 6, 9)
    >>> tools.accumulate_from_n((4, 2, 3), 2)
    (2, 6, 8, 11)
    """
    return itertools.accumulate(itertools.chain((n,), iterable))


def accumulate_from_zero(iterable: typing.Iterable[constants.Real]) -> typing.Iterator:
    """Accumulates iterable starting from 0.

    :param iterable: The iterable which values shall be accumulated.

    **Example:**

    >>> from mutwo.utilities import tools
    >>> tools.accumulate_from_zero((4, 2, 3), 0)
    (0, 4, 6, 9)
    """
    return accumulate_from_n(iterable, 0)


def insert_next_to(
    iterable: typing.MutableSequence,
    item_to_find: typing.Any,
    distance: int,
    item_to_insert: typing.Any,
):
    """Insert an item into a list relative to the first item equal to a certain value."""

    index = list(iterable).index(item_to_find)
    if distance == 0:
        iterable[index] = item_to_insert
    else:
        real_distance = distance + 1 if distance < 0 else distance
        iterable.insert(index + real_distance, item_to_insert)


T = typing.TypeVar("T", bound=constants.Real)


def find_closest_index(
    item: constants.Real,
    data: typing.Iterable,
    key: typing.Callable[[typing.Any], T] = lambda item: item,
) -> int:
    """Return index of element in ``data`` with smallest difference to ``item``.

    :param item: The item from which the closest item shall be found.
    :param data: The data to which the closest item shall be found.

    **Example:**

    >>> from mutwo.utilities import tools
    >>> tools.find_closest_index(2, (1, 4, 5))
    0
    >>> tools.find_closest_index(127, (100, 4, 300, 53, 129))
    4
    >>> tools.find_closest_index(127, (('hi', 100), ('hey', 4), ('hello', 300)), key=lambda item: item[1])
    0
    """

    research_data = tuple(map(key, data))
    sorted_research_data = sorted(research_data)

    solution = bisect.bisect_left(sorted_research_data, item)
    # make type ignore because data has been converted to tuple (which is sizeable)
    if solution == len(data):  # type: ignore
        index = solution - 1

    elif solution == 0:
        index = solution

    else:
        indices = (solution, solution - 1)
        differences = tuple(abs(-sorted_research_data[n] + item) for n in indices)
        index = indices[differences.index(min(differences))]  # type: ignore

    return research_data.index(sorted_research_data[index])


def find_closest_item(
    item: constants.Real,
    data: typing.Sequence,
    key: typing.Callable[[typing.Any], T] = lambda item: item,
) -> T:
    """Return element in ``data`` with smallest difference to ``item``.

    :param item: The item from which the closest item shall be found.
    :param data: The data to which the closest item shall be found.
    :return: The closest number to ``item`` in ``data``.

    **Example:**

    >>> from mutwo.utilities import tools
    >>> tools.find_closest_item(2, (1, 4, 5))
    1
    >>> tools.find_closest_item(127, (100, 4, 300, 53, 129))
    129
    >>> tools.find_closest_item(127, (('hi', 100), ('hey', 4), ('hello', 300)), key=lambda item: item[1])
    ('hi', 100)
    """
    return data[find_closest_index(item, data, key=key)]


def import_module_if_dependencies_have_been_installed(
    module: str, dependencies: tuple[str, ...], import_class: bool = False
) -> None:
    for dependency in dependencies:
        if not importlib.util.find_spec(dependency):
            message = (
                "Can't load module '{0}'. Install dependency '{1}' if you want to use"
                " '{0}'.".format(module, dependency)
            )
            warnings.warn(message)
            return

    if import_class:
        class_name = module.split(".")[-1]
        return getattr(importlib.import_module(module), class_name)

    else:
        importlib.import_module(module)


def uniqify_iterable(
    iterable: typing.Sequence,
    sort_key: typing.Callable[[typing.Any], constants.Real] = None,
    group_by_key: typing.Callable[[typing.Any], typing.Any] = None,
) -> typing.Iterable:
    """Not-Order preserving function to uniqify any iterable with non-hashable objects.

    :param iterable: The iterable which items shall be uniqified.
    :return: Return uniqified version of the entered iterable.
        The function will try to return the same type of the passed
        iterable. If Python raises an error during initialisation of
        the original iterable type, the function will simply return
        a tuple.

    **Example:**

    >>> from mutwo.parameters import pitches
    >>> from mutwo.utilities import tools
    >>> tools.uniqify_iterable([pitches.WesternPitch(pitch_name) for pitch_name in 'c d e c d e e f a c a'.split(' ')])
    [WesternPitch(c4),
    WesternPitch(d4),
    WesternPitch(e4),
    WesternPitch(f4),
    WesternPitch(a4)]
    """

    sorted_iterable = sorted(iterable, key=sort_key)
    result = (key for key, _ in itertools.groupby(sorted_iterable, key=group_by_key))

    try:
        return type(iterable)(result)  # type: ignore

    except Exception:
        return tuple(result)


def cyclic_permutations(sequence: typing.Sequence[typing.Any]) -> typing.Generator:
    """Cyclic permutation of an iterable. Return a generator object.

    :param sequence: The sequence from which cyclic permutations shall be generated.

    **Example:**

    >>> from mutwo.utilities import tools
    >>> permutations = tools.cyclic_permutations((1, 2, 3, 4))
    >>> next(permutations)
    (2, 3, 4, 1)
    >>> next(permutations)
    (3, 4, 1, 2)

    `Adapted function from the reply of Paritosh Singh
    <https://stackoverflow.com/questions/56171246/cyclic-permutation-operators-in-python/56171531>`_
    """

    def reorder_from_index(index: int, sequence: tuple) -> tuple:
        return sequence[index:] + sequence[:index]

    return (
        functools.partial(reorder_from_index, i)(sequence) for i in range(len(sequence))
    )


def camel_case_to_snake_case(camel_case_string: str) -> str:
    """Transform camel case formatted string to snake case.

    :param camel_case_string: String which is formatted using
        camel case (no whitespace, but upper letters at
        new word start).
    :return: string formatted using snake case

    **Example:** MyClassName -> my_class_name
    """

    characters = []

    is_first = True
    for character in camel_case_string:
        if character.isupper():
            character = character.lower()
            if not is_first:
                character = "_{}".format(character)

        if is_first:
            is_first = False

        characters.append(character)

    return "".join(characters)


def get_nested_item_from_indices(
    indices: typing.Sequence[int], sequence: typing.Sequence
) -> typing.Any:
    """Get item in nested Sequence.

    :param indices: The indices of the nested item.
    :type indices: typing.Sequence[int]
    :param sequence: A nested sequence.
    :type sequence: typing.Sequence[typing.Any]


    **Example:**

    >>> from mutwo.utilities import tools
    >>> nested_sequence = (1, 2, (4, (5, 1), (9, (3,))))
    >>> tools.get_nested_item_from_indices((2, 2, 0), nested_sequence)
    9
    >>> nested_sequence[2][2][0]  # is equal
    9
    """

    for index in indices:
        sequence = sequence[index]
    return sequence


def set_nested_item_from_indices(
    indices: typing.Sequence[int],
    sequence: typing.MutableSequence,
    item: typing.Any,
) -> None:
    """Set item in nested Sequence.

    :param indices: The indices of the nested item which shall be set.
    :type indices: typing.Sequence[int]
    :param sequence: A nested sequence.
    :type sequence: typing.MutableSequence[typing.Any]
    :param item: The new item value.
    :type item: typing.Any

    **Example:**

    >>> from mutwo.utilities import tools
    >>> nested_sequence = [1, 2, [4, [5, 1], [9, [3]]]]]
    >>> tools.set_nested_item_from_indices((2, 2, 0), nested_sequence, 100)
    >>> nested_sequence[2][2][0] = 100  # is equal
    """

    n_indices = len(indices)
    for nth_index, index in enumerate(indices):
        if n_indices == nth_index + 1:
            sequence.__setitem__(index, item)
        else:
            sequence = sequence[index]


def round_floats(number_to_round: constants.Real, n_digits: int) -> constants.Real:
    """Round number if it is an instance of float, otherwise unaltered number.

    :param number_to_round: The number which shall be rounded.
    :type number_to_round: constants.Real
    :param n_digits: How many digits shall the number be rounded.
    :type n_digits: int
    """

    if isinstance(number_to_round, float):
        return round(number_to_round, n_digits)
    else:
        return number_to_round


def find_numbers_which_sums_up_to(
    given_sum: float,
    numbers_to_choose_from: typing.Optional[typing.Sequence[float]] = None,
    n_items_to_sum_up: typing.Optional[set[int]] = None,
) -> tuple[tuple[float, ...], ...]:
    """Find all combinations of numbers which sum is equal to the given sum.

    :param given_sum: The target sum for which different combinations shall
        be searched.
    :type given_sum: float
    :param numbers_to_choose_from: A sequence of numbers which shall be
        tried to combine to result in the :attr:`given_sum`. If the user
        doesn't specify this argument mutwo will use all natural numbers
        equal or smaller than the :attr:`given_sum`.
    :type numbers_to_choose_from: typing.Optional[typing.Sequence[float]]
    :param n_items_to_sum_up: How many numbers can be combined to result
        in the :attr:`given_sum`. If the user doesn't specify this argument
        mutwo will use all natural numbers equal or smaller than the
        :attr:`given_sum`.
    :type n_items_to_sum_up: typing.Optional[set[int]]

    **Example:**

    >>> from mutwo.utilities import tools
    >>> tools.find_numbers_which_sums_up_to(4)
    ((4,), (1, 3), (2, 2), (1, 1, 2), (1, 1, 1, 1))
    """

    if not numbers_to_choose_from:
        numbers_to_choose_from = tuple(range(1, int(given_sum) + 1))

    if not n_items_to_sum_up:
        n_items_to_sum_up = set(range(1, given_sum + 1))

    numbers = []
    for n_items in n_items_to_sum_up:
        numbers.extend(
            [
                pair
                for pair in itertools.combinations_with_replacement(
                    numbers_to_choose_from, n_items
                )
                if sum(pair) == given_sum
            ]
        )
    return tuple(numbers)


def call_function_except_attribute_error(
    function: typing.Callable[[typing.Any], typing.Any],
    argument: typing.Any,
    exception_value: typing.Any,
) -> typing.Any:
    """Run a function with argument as input

    :param function: The function to be called.
    :param argument: The argument with which the function shall be called.
    :param exception_value: The alternative value if the function call raises an
        `AttributeError`.
    :return: Return :obj:`exception_value` in case an attribute error occurs.
        In case the function call is successful the function return value will
        be returned.
    """

    try:
        value = function(argument)
    except AttributeError:
        value = exception_value

    return value
