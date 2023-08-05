import pytest
from ..openapi_data_generator.OptionalCombinationGenerator import generate_all_possible_objects
from ..openapi_data_generator.ObjectGenerator import ObjectsGenerator
from compare_objects import compare_objects
from openapi_schema_generator import OpenApiSchemaValidator, OpenApiSchemaGenerator

src_path = "test/Examples"
validator_jobs = OpenApiSchemaValidator(f"{src_path}/jobs.json")
jobs_schemas = OpenApiSchemaGenerator(f"{src_path}/jobs.json").build_mapped_schema()
validator_petstore = OpenApiSchemaValidator(f"{src_path}/petstore.json")
petstore_schemas = OpenApiSchemaGenerator(f"{src_path}/petstore.json").build_mapped_schema()

config = {'default_probability': 5, 'nullable_probability': 5, 'array_min_items': 0, 'array_max_items': 5,
          'min_str_len': 1, 'max_str_len': 10, 'min_int': -2147483648, 'max_int': 2147483647,
          'min_float': 3.4 * pow(10, -38), 'max_float': 3.4 * pow(10, 38)}


# ~~~~~~~~~~~~~~~~~~~~~ TEST NATIVE ~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def test_two_natives_val_compare():
    result = generate_all_possible_objects("require", "full")
    assert compare_objects(result, ["require", "full"])


def test_native_and_list_val_compare():
    result = generate_all_possible_objects("require", ['native', 'full'])
    assert compare_objects(result, ["require", ['native', 'full']])


def test_two_list_of_native():
    result = generate_all_possible_objects({'native', "require"}, ['native', 'full'])
    assert compare_objects(result, [{'native', "require"}, ['native', 'full']])


def test_list_and_longer_list_of_native():
    result = generate_all_possible_objects([('native',), "require"], ['native', 'full', 'longer'])
    assert compare_objects(result, [[('native',), "require"], ['native', 'full', 'longer']])


def test_list_and_longer_with_diff_list_of_native():
    result = generate_all_possible_objects(['native', "require", 'longer'], ['native', 'full'])
    assert compare_objects(result, [['native', 'require', 'longer'], ['native', 'full']])


# ~~~~~~~~~~~~~~~~~~~~~ TEST DICT ~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def test_single_case_to_dicts():
    result = generate_all_possible_objects({"a": 1}, {"a": 1, "b": 2})
    assert compare_objects(result, [{"a": 1}, {"a": 1, "b": 2}])


def test_two_equal_dicts():
    result = generate_all_possible_objects({"a": 1}, {"a": 1})
    assert compare_objects(result, [{"a": 1}])


def test_two_bigger_equal_dict():
    result = generate_all_possible_objects({"a": 1, "b": 2}, {"a": 1, "b": 2})
    assert compare_objects(result, [{"a": 1, "b": 2}])


def test_diff_of_two_keys():
    result = generate_all_possible_objects({"a": 1}, {"a": 1, "b": 2, "c": 3})
    assert compare_objects(result, [{'a': 1}, {'a': 1, 'c': 3}, {'a': 1, 'b': 2}, {'a': 1, 'b': 2, 'c': 3}])


def test_two_keys_equal_value_not_equal():
    result = generate_all_possible_objects({"a": 1, "b": 2}, {"a": 1, "b": 3})
    assert compare_objects(result, [{'a': 1, 'b': 3}])


# ~~~~~~~~~~~~~~~~~~~~~ TEST DICT WITH DICT INSIDE ~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def test_require_have_nested_key():
    result = generate_all_possible_objects({"a": 1, "b": {"a": 1}}, {"a": 1, "b": {"a": 1, "b": 2}})
    expected = [{'a': 1, 'b': {'a': 1}}, {'a': 1, 'b': {'a': 1, 'b': 2}}]
    assert compare_objects(result, expected)


def test_require_nested_has_key_full_doesnt_have():
    result = generate_all_possible_objects({"a": 1, "b": {"a": 1}}, {"a": 1, "b": {"a": 1, "b": 2}})
    expected = [{'a': 1, 'b': {'a': 1}}, {'a': 1, 'b': {'a': 1, 'b': 2}}]
    assert compare_objects(result, expected)


def test_require_does_not_have_nested_key():
    result = generate_all_possible_objects({"a": 1}, {"a": 1, "b": {"a": 1, "b": 2}})
    expected = [{'a': 1}, {'a': 1, 'b': {'b': 2}}, {'a': 1, 'b': {'a': 1}}, {'a': 1, 'b': {'a': 1, 'b': 2}}]
    assert compare_objects(result, expected)


def test_very_nested_dict():
    result = generate_all_possible_objects({"a": {"b": {"c": {"d": 1}}}}, {"a": {"b": {"c": {"d": 1, "e": 2, "f": 3}}}})
    expected = [{'a': {'b': {'c': {'d': 1}}}},
                {'a': {'b': {'c': {'d': 1, 'f': 3}}}},
                {'a': {'b': {'c': {'d': 1, 'e': 2}}}},
                {'a': {'b': {'c': {'d': 1, 'e': 2, 'f': 3}}}}]
    assert compare_objects(result, expected)


# ~~~~~~~~~~~~~~~~~~~~~ TEST DICT WITH LIST INSIDE ~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def test_require_have_nested_list():
    result = generate_all_possible_objects({"a": 1, "b": [{"a": 1}]}, {"a": 1, "b": [{"a": 1, "b": 2}]})
    expected = [{'a': 1, 'b': [{'a': 1}]}, {'a': 1, 'b': [{'a': 1, 'b': 2}]}]
    assert compare_objects(result, expected)


def test_list_have_not_exist_object_at_require():
    result = generate_all_possible_objects({"a": 1, "b": [{"a": 1}]}, {"a": 1, "b": [{"a": 1}, {"b": 2, 'c': 3}]})
    expected = [{'a': 1, 'b': [{'a': 1}]}, {'a': 1, 'b': [{'a': 1}, {'b': 2}]}, {'a': 1, 'b': [{'a': 1}, {'c': 3}]},
                {'a': 1, 'b': [{'a': 1}, {'b': 2, 'c': 3}]}]

    assert compare_objects(result, expected)


def test_require_have_nested_list_with_bigger_object():
    result = generate_all_possible_objects({"a": 1, "b": [{"a": 1}]}, {"a": 1, "b": [{"a": 1, "b": 2, "c": 4}]})
    expected = [{'a': 1, 'b': [{'a': 1}]}, {'a': 1, 'b': [{'a': 1, 'b': 2}]}, {'a': 1, 'b': [{'a': 1, 'c': 4}]},
                {'a': 1, 'b': [{'a': 1, 'b': 2, 'c': 4}]}]
    assert compare_objects(result, expected)


def test_require_have_nested_list_and_dict():
    result = generate_all_possible_objects({"a": 1, "b": [{"a": 1}]}, {"a": 1, "b": [{"a": 1, "b": 2}], "c": {"e": 1}})
    expected = [{'a': 1, 'b': [{'a': 1}]}, {'a': 1, 'b': [{'a': 1, 'b': 2}], 'c': {}},
                {'a': 1, 'b': [{'a': 1}], 'c': {'e': 1}},
                {'a': 1, 'b': [{'a': 1, 'b': 2}], 'c': {'e': 1}}]
    assert compare_objects(result, expected)


def test_nested_dict_with_nested_list():
    result = generate_all_possible_objects({"a": 1, "n": {"b": [{"a": 1}]}},
                                           {"a": 1, "n": {"b": [{"a": 1, "b": 2, "c": 3}]}})
    expected = [{'a': 1, 'n': {'b': [{'a': 1}]}}, {'a': 1, 'n': {'b': [{'a': 1, 'b': 2}]}},
                {'a': 1, 'n': {'b': [{'a': 1, 'c': 3}]}}, {'a': 1, 'n': {'b': [{'a': 1, 'b': 2, 'c': 3}]}}]
    assert compare_objects(result, expected)


def test_nested_list_with_nested_dict_with_nest_list():
    result = generate_all_possible_objects({"a": 1, "n": [{"b": [{"a": 1}]}]},
                                           {"a": 1, "n": [{"b": [{"a": 1}, {"b": 2, "c": 3}]}]})
    expected = [{'a': 1, 'n': [{'b': [{'a': 1}]}]}, {'a': 1, 'n': [{'b': [{'a': 1}, {'b': 2}]}]},
                {'a': 1, 'n': [{'b': [{'a': 1}, {'c': 3}]}]}, {'a': 1, 'n': [{'b': [{'a': 1}, {'b': 2, 'c': 3}]}]}]
    assert compare_objects(result, expected)


# ~~~~~~~~~~~~~~~~~~~~~ TEST WITH SCHEMAS  ~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~ JOBS  ~~~~~~~~~~~~~~~~~~~~~~~~~~ #

@pytest.mark.parametrize('curr_key', list(jobs_schemas.keys()))
def test_object_build_successfully_with_schema_jobs(curr_key):
    if "post" in jobs_schemas[curr_key] and "requestBody" in jobs_schemas[curr_key]['post']:
        schema = jobs_schemas[curr_key]['post']['requestBody']
        obj = ObjectsGenerator(schema, config)
        optional_list = generate_all_possible_objects(obj.required_object, obj.full_object, schema)
        for obj in optional_list:
            assert validator_jobs.validate_request_schema(curr_key, obj)


# ~~~~~~~~~~~~~~~~~~~~~ PET STORE  ~~~~~~~~~~~~~~~~~~~~~~~~~~ #
@pytest.mark.parametrize('curr_key', list(petstore_schemas.keys()))
def test_object_build_successfully_with_schema_petstore(curr_key):
    if "post" in petstore_schemas[curr_key] and "requestBody" in petstore_schemas[curr_key]['post']:
        schema = petstore_schemas[curr_key]['post']['requestBody']
        obj = ObjectsGenerator(schema, config)
        optional_list = generate_all_possible_objects(obj.required_object, obj.full_object, schema)
        for obj in optional_list:
            assert validator_petstore.validate_request_schema(curr_key, obj)
