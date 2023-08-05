from ..openapi_data_generator.ObjectGenerator import ObjectsGenerator
from openapi_schema_generator import OpenApiSchemaValidator, OpenApiSchemaGenerator
import pytest

src_path = "test/Examples"
validator_jobs = OpenApiSchemaValidator(f"{src_path}/jobs.json")
jobs_schemas = OpenApiSchemaGenerator(f"{src_path}/jobs.json").build_mapped_schema()
validator_petstore = OpenApiSchemaValidator(f"{src_path}/petstore.json")
petstore_schemas = OpenApiSchemaGenerator(f"{src_path}/petstore.json").build_mapped_schema()

config = {'default_probability': 5, 'nullable_probability': 5, 'array_min_items': 0, 'array_max_items': 5,
          'min_str_len': 1, 'max_str_len': 10, 'min_int': -2147483648, 'max_int': 2147483647,
          'min_float': 3.4 * pow(10, -38), 'max_float': 3.4 * pow(10, 38)}


def get_certain_schema(schemas, curr_key):
    data = schemas[curr_key].get('post', None)
    if data:
        return data.get('requestBody', None)


# ~~~~~~~~~~~~~~~~~~~~~ JOBS  ~~~~~~~~~~~~~~~~~~~~~~~~~~ #

@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_object_generate_require(curr_key):
    schema = get_certain_schema(jobs_schemas, curr_key)
    if schema:
        gen = ObjectsGenerator(schema, config)
        assert validator_jobs.validate_request_schema(curr_key, gen.required_object)


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_object_generate_full(curr_key):
    schema = get_certain_schema(jobs_schemas, curr_key)
    if schema:
        gen = ObjectsGenerator(schema, config)
        assert validator_jobs.validate_request_schema(curr_key, gen.full_object)


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_object_generate_min_val(curr_key):
    schema = get_certain_schema(jobs_schemas, curr_key)
    if schema:
        gen = ObjectsGenerator(schema, config)
        assert validator_jobs.validate_request_schema(curr_key, gen.min_val_object)


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_invalid_object(curr_key):
    schema = get_certain_schema(jobs_schemas, curr_key)
    if schema:
        gen = ObjectsGenerator(schema, config, generate_invalid=True)
        for elem in gen.invalid_objects:
            assert validator_jobs.validate_request_schema(curr_key, elem) is False


# ~~~~~~~~~~~~~~~~~~~~~ PET STORE  ~~~~~~~~~~~~~~~~~~~~~~~~~~ #


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_object_generate_require(curr_key):
    schema = get_certain_schema(petstore_schemas, curr_key)
    if schema:
        gen = ObjectsGenerator(schema, config)
        assert validator_petstore.validate_request_schema(curr_key, gen.required_object)


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_object_generate_full(curr_key):
    schema = get_certain_schema(petstore_schemas, curr_key)
    if schema:
        gen = ObjectsGenerator(schema, config)
        assert validator_petstore.validate_request_schema(curr_key, gen.full_object)


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_object_generate_min_val(curr_key):
    schema = get_certain_schema(petstore_schemas, curr_key)
    if schema:
        gen = ObjectsGenerator(schema, config)
        assert validator_petstore.validate_request_schema(curr_key, gen.min_val_object)


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_invalid_object(curr_key):
    schema = get_certain_schema(petstore_schemas, curr_key)
    if schema:
        gen = ObjectsGenerator(schema, config, generate_invalid=True)
        for elem in gen.invalid_objects:
            assert not validator_petstore.validate_request_schema(curr_key, elem['data'])

