from ..src.ObjectsHandler import remove_keys_from_data
from compare_objects import compare_objects


# ******** Test remove keys ******** #

def test_remove_single_object():
    data = {"a": 1, "b": 2}
    keys = ['b']
    assert compare_objects(remove_keys_from_data(data, keys), {'a': 1})


def test_remove_nested_object():
    data = {"a": 1, "b": {'c': 1, "d": 2}}
    keys = ['b:d']
    assert compare_objects(remove_keys_from_data(data, keys), {"a": 1, "b": {'c': 1}})


def test_remove_two_keys_object():
    data = {"a": 1, "b": {'c': 1, "d": 2}}
    keys = ['a', 'b:d']
    assert compare_objects(remove_keys_from_data(data, keys), {"b": {'c': 1}})


def test_remove_nested_list_of_object():
    data = {"a": 1, "b": [{'c': 1, "d": 2}, {'c': 1, "d": 2}, {'c': 1, "d": 2}]}
    keys = ['a', 'b-d']
    assert compare_objects(remove_keys_from_data(data, keys), {"b": [{'c': 1}, {'c': 1}, {'c': 1}]})


def test_remove_list_of_objects():
    data = [{"a": 1, "b": 2}, {"a": 1, "b": 2}]
    keys = ['b']
    assert compare_objects(remove_keys_from_data(data, keys), [{"a": 1}, {"a": 1}])


def test_remove_nested_list_with_nested_list_of_objects():
    data = [{"a": 1, "b": [{"d": 3, "r": {"y": 4, "l": [{'f': 3, 'g': 5}, {'f': 3, 'g': 5}]}},
                           {"d": 3, "r": {"y": 4, "l": [{'f': 3, 'g': 5}, {'f': 3, 'g': 5}]}}]},
            {"a": 1, "b": [{"d": 3, "r": {"y": 4, "l": [{'f': 3, 'g': 5}, {'f': 3, 'g': 5}]}},
                           {"d": 3, "r": {"y": 4, "l": [{'f': 3, 'g': 5}, {'f': 3, 'g': 5}]}}]}]
    keys = ['a', "b-r:y", 'b-r:l-g']
    expected = [{"b": [{"d": 3, "r": {"l": [{'f': 3}, {'f': 3}]}}, {"d": 3, "r": {"l": [{'f': 3}, {'f': 3}]}}]},
                {"b": [{"d": 3, "r": {"l": [{'f': 3}, {'f': 3}]}}, {"d": 3, "r": {"l": [{'f': 3}, {'f': 3}]}}]}]
    assert compare_objects(remove_keys_from_data(data, keys), expected)
