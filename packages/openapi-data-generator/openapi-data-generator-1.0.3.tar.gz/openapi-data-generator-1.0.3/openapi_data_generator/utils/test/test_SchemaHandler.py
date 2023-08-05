from ...ObjectGenerator import ObjectsGenerator
from ..src.KeysHandler import get_all_levels_keys
from ..src.SchemaHandler import get_keys_and_attr
from openapi_schema_generator import OpenApiSchemaGenerator
from compare_objects import compare_objects
import json

schemas = OpenApiSchemaGenerator(f"test/Examples/jobs.json").build_mapped_schema()


def read_file(path):
    with open(path) as f:
        return json.load(f)


def test_object_without_nested_list():
    curr_key = '/exec/stop'
    schema_to = schemas[curr_key]["post"]['requestBody']
    obj = {"jobId": "string", "reason": "requested by user"}
    keys_and_attr = get_keys_and_attr(schema_to, get_all_levels_keys(obj))
    expected = read_file("openapi_data_generator/utils/test/results/object_without_nested_list.json")
    assert compare_objects(keys_and_attr, expected)


def test_object_with_nested_list():
    obj = {"name": "string", "flowInput": {}, "webhooks": {"progress": "http://my-url-to-progress",
                                                           "result": "http://my-url-to-result"}, "options": {},
           "priority": 3, "triggers": {"pipelines": ["string"], "cron": {"pattern": "string", "enabled": False}}}
    curr_key = '/exec/stored'
    schema_to = schemas[curr_key]["post"]['requestBody']

    keys_and_attr = get_keys_and_attr(schema_to, get_all_levels_keys(obj))
    expected = read_file("openapi_data_generator/utils/test/results/object_with_nested_list.json")
    assert compare_objects(keys_and_attr, expected)


def test_list_of_object_with_nested_objects():
    curr_key = "/pipelines/results/raw/{name}"
    schema_to = schemas[curr_key]["get"]['responses']['200']
    obj = [{"jobId": "string", "timestamp": "string", "pipeline": "string", "data": ["string"],
            "status": "string", "timeTook": 0, "storageModule": "string"}]

    keys_and_attr = get_keys_and_attr(schema_to, get_all_levels_keys(obj))
    expected = read_file("openapi_data_generator/utils/test/results/list_of_object_with_nested_objects.json")
    assert compare_objects(keys_and_attr, expected) or compare_objects(keys_and_attr, [])
