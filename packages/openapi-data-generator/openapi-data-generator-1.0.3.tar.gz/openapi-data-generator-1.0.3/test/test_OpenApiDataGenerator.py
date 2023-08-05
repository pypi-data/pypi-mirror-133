from ..openapi_data_generator.OpenApiDataGenerator import OpenApiDataGenerator
from openapi_schema_generator import OpenApiSchemaValidator, OpenApiSchemaGenerator
import pytest

# *********************** GLOBALS ALL FUNCTIONALITY OF METHODS ************************ #

src_path = "test/Examples"

validator_jobs = OpenApiSchemaValidator(f"{src_path}/jobs.json")
jobs_schemas = OpenApiSchemaGenerator(f"{src_path}/jobs.json").build_mapped_schema()
jobs_generator = OpenApiDataGenerator(f"{src_path}/jobs.json", generate_invalid=True, generate_responses=True)

validator_petstore = OpenApiSchemaValidator(f"{src_path}/petstore.json")
petstore_generator = OpenApiDataGenerator(f"{src_path}/petstore.json", generate_invalid=True, generate_responses=True)
petstore_schemas = OpenApiSchemaGenerator(f"{src_path}/petstore.json").build_mapped_schema()

new_value = "new_value"
new_field = "new_field"


# ****************** REQUEST ******************** #

# ~~~~~~ REQUIRE ~~~~ #

@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_assert_require_is_valid_request_post_jobs(curr_key):
    object_to_test = jobs_generator.get_required_request_object(curr_key, "post")
    assert validator_jobs.validate_request_schema(curr_key, object_to_test, "post")


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_assert_require_is_valid_request_put_jobs(curr_key):
    object_to_test = jobs_generator.get_required_request_object(curr_key, "put")
    assert validator_jobs.validate_request_schema(curr_key, object_to_test, "put")


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_assert_require_is_valid_request_get_jobs(curr_key):
    object_to_test = jobs_generator.get_required_request_object(curr_key, "get")
    assert validator_jobs.validate_request_schema(curr_key, object_to_test, "get")


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_assert_require_is_valid_request_delete_jobs(curr_key):
    object_to_test = jobs_generator.get_required_request_object(curr_key, "delete")
    assert validator_jobs.validate_request_schema(curr_key, object_to_test, "delete")


# ~~~~~~ FULL ~~~~ #


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_assert_full_is_valid_request_post_jobs(curr_key):
    object_to_test = jobs_generator.get_full_request_object(curr_key, "post")
    assert validator_jobs.validate_request_schema(curr_key, object_to_test, "post")


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_assert_full_is_valid_request_put_jobs(curr_key):
    object_to_test = jobs_generator.get_full_request_object(curr_key, "put")
    assert validator_jobs.validate_request_schema(curr_key, object_to_test, "put")


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_assert_full_is_valid_request_get_jobs(curr_key):
    object_to_test = jobs_generator.get_full_request_object(curr_key, "get")
    assert validator_jobs.validate_request_schema(curr_key, object_to_test, "get")


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_assert_full_is_valid_request_delete_jobs(curr_key):
    object_to_test = jobs_generator.get_full_request_object(curr_key, "delete")
    assert validator_jobs.validate_request_schema(curr_key, object_to_test, "delete")


# ~~~~~~ RANDOM  ~~~~ #


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_assert_all_random_is_valid_request_post_jobs(curr_key):
    full_list_ob_objects = jobs_generator.get_all_possible_request_objects(curr_key, "post")
    if full_list_ob_objects:
        for elem in full_list_ob_objects:
            assert validator_jobs.validate_request_schema(curr_key, elem, "post")


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_assert_all_random_is_valid_request_get_jobs(curr_key):
    full_list_ob_objects = jobs_generator.get_all_possible_request_objects(curr_key, "get")
    if full_list_ob_objects:
        for elem in full_list_ob_objects:
            assert validator_jobs.validate_request_schema(curr_key, elem, "get")


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_assert_all_random_is_valid_request_put_jobs(curr_key):
    full_list_ob_objects = jobs_generator.get_all_possible_request_objects(curr_key, "put")
    if full_list_ob_objects:
        for elem in full_list_ob_objects:
            assert validator_jobs.validate_request_schema(curr_key, elem, "put")


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_assert_all_random_is_valid_request_delete_jobs(curr_key):
    full_list_ob_objects = jobs_generator.get_all_possible_request_objects(curr_key, "delete")
    if full_list_ob_objects:
        for elem in full_list_ob_objects:
            assert validator_jobs.validate_request_schema(curr_key, elem, "delete")


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_invalid_request_object(curr_key):
    gen_obj = jobs_generator.get_invalid_request_object(curr_key)
    if gen_obj:
        assert not validator_jobs.validate_request_schema(curr_key, gen_obj)
    else:
        assert True


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_invalid_all_request_object(curr_key):
    full_list_ob_objects = jobs_generator.get_all_invalid_request_objects(curr_key)
    if full_list_ob_objects:
        for elem in full_list_ob_objects:
            if elem:
                assert not validator_jobs.validate_request_schema(curr_key, elem)
            else:
                assert True


# ****************** RESPONSE ******************** #

# ~~~~~~ REQUIRE ~~~~ #

@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_assert_require_is_valid_response_post_jobs(curr_key):
    object_to_test = jobs_generator.get_required_response_object(curr_key, "post")
    assert validator_jobs.validate_response_schema(curr_key, object_to_test, "post")


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_assert_require_is_valid_response_put_jobs(curr_key):
    object_to_test = jobs_generator.get_required_response_object(curr_key, "put")
    assert validator_jobs.validate_response_schema(curr_key, object_to_test, "put")


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_assert_require_is_valid_response_get_jobs(curr_key):
    object_to_test = jobs_generator.get_required_response_object(curr_key, "get")
    assert validator_jobs.validate_response_schema(curr_key, object_to_test, "get")


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_assert_require_is_valid_response_delete_jobs(curr_key):
    object_to_test = jobs_generator.get_required_response_object(curr_key, "delete")
    assert validator_jobs.validate_response_schema(curr_key, object_to_test, "delete")


# ~~~~~~ FULL ~~~~ #


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_assert_full_is_valid_response_post_jobs(curr_key):
    object_to_test = jobs_generator.get_full_response_object(curr_key, "post")
    assert validator_jobs.validate_response_schema(curr_key, object_to_test, "post")


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_assert_require_is_valid_response_put_jobs(curr_key):
    object_to_test = jobs_generator.get_full_response_object(curr_key, "put")
    assert validator_jobs.validate_response_schema(curr_key, object_to_test, "put")


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_assert_require_is_valid_response_get_jobs(curr_key):
    object_to_test = jobs_generator.get_full_response_object(curr_key, "get")
    assert validator_jobs.validate_response_schema(curr_key, object_to_test, "get")


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_assert_require_is_valid_response_delete_jobs(curr_key):
    object_to_test = jobs_generator.get_full_response_object(curr_key, "delete")
    assert validator_jobs.validate_response_schema(curr_key, object_to_test, "delete")


# ~~~~~~ RANDOM  ~~~~ #

@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_assert_all_random_is_valid_response_post_jobs(curr_key):
    full_list_ob_objects = jobs_generator.get_all_possible_response_objects(curr_key, 'post')
    if full_list_ob_objects:
        for elem in full_list_ob_objects:
            assert validator_jobs.validate_response_schema(curr_key, elem, "post")


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_assert_all_random_is_valid_response_get_jobs(curr_key):
    full_list_ob_objects = jobs_generator.get_all_possible_response_objects(curr_key, "get")
    if full_list_ob_objects:
        for elem in full_list_ob_objects:
            assert validator_jobs.validate_response_schema(curr_key, elem, "get")


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_assert_all_random_is_valid_response_put_jobs(curr_key):
    full_list_ob_objects = jobs_generator.get_all_possible_response_objects(curr_key, "put")
    if full_list_ob_objects:
        for elem in full_list_ob_objects:
            assert validator_jobs.validate_response_schema(curr_key, elem, "put")


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_assert_all_random_is_valid_response_delete_jobs(curr_key):
    full_list_ob_objects = jobs_generator.get_all_possible_response_objects(curr_key, "delete")
    if full_list_ob_objects:
        for elem in full_list_ob_objects:
            assert validator_jobs.validate_response_schema(curr_key, elem, "delete")


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_invalid_response_object(curr_key):
    gen_obj = jobs_generator.get_invalid_response_object(curr_key)
    if gen_obj:
        assert not validator_jobs.validate_response_schema(curr_key, gen_obj)
    else:
        assert True


@pytest.mark.parametrize("curr_key", list(jobs_schemas.keys()))
def test_invalid_all_response_object(curr_key):
    full_list_ob_objects = jobs_generator.get_all_invalid_response_objects(curr_key)
    if full_list_ob_objects:
        for elem in full_list_ob_objects:
            if elem:
                if isinstance(elem, list) and len(elem) > 0:
                    assert True
                else:
                    assert not validator_jobs.validate_response_schema(curr_key, elem)


# *********************** TEST ALL ENDPOINTS WITH ALL VARIATION VERSION 2.4 ************************ #

# ****************** REQUEST ******************** #


# ~~~~~~ REQUIRE ~~~~ #

@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_assert_require_is_valid_request_post_v_24(curr_key):
    object_to_test = petstore_generator.get_required_request_object(curr_key, "post")
    validator_petstore.validate_request_schema(curr_key, object_to_test, "post")
    assert True


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_assert_require_is_valid_request_put_v_24(curr_key):
    object_to_test = petstore_generator.get_required_request_object(curr_key, "put")
    validator_petstore.validate_request_schema(curr_key, object_to_test, "put")
    assert True


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_assert_require_is_valid_request_get_v_24(curr_key):
    object_to_test = petstore_generator.get_required_request_object(curr_key, "get")
    validator_petstore.validate_request_schema(curr_key, object_to_test, "get")
    assert True


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_assert_require_is_valid_request_delete_v_24(curr_key):
    object_to_test = petstore_generator.get_required_request_object(curr_key, "delete")
    validator_petstore.validate_request_schema(curr_key, object_to_test, "delete")
    assert True


# ~~~~~~ FULL ~~~~ #


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_assert_full_is_valid_request_post_v_24(curr_key):
    object_to_test = petstore_generator.get_full_request_object(curr_key, "post")
    validator_petstore.validate_request_schema(curr_key, object_to_test, "post")
    assert True


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_assert_full_is_valid_request_put_v_24(curr_key):
    object_to_test = petstore_generator.get_full_request_object(curr_key, "put")
    validator_petstore.validate_request_schema(curr_key, object_to_test, "put")
    assert True


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_assert_full_is_valid_request_get_v_24(curr_key):
    object_to_test = petstore_generator.get_full_request_object(curr_key, "get")
    validator_petstore.validate_request_schema(curr_key, object_to_test, "get")
    assert True


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_assert_full_is_valid_request_delete_v_24(curr_key):
    object_to_test = petstore_generator.get_full_request_object(curr_key, "delete")
    validator_petstore.validate_request_schema(curr_key, object_to_test, "delete")
    assert True


# ~~~~~~ RANDOM  ~~~~ #


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_assert_all_random_is_valid_request_post_v_24(curr_key):
    full_list_ob_objects = petstore_generator.get_all_possible_request_objects(curr_key, "post")
    if full_list_ob_objects:
        for elem in full_list_ob_objects:
            validator_petstore.validate_request_schema(curr_key, elem, "post")
    assert True


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_assert_all_random_is_valid_request_get_v_24(curr_key):
    full_list_ob_objects = petstore_generator.get_all_possible_request_objects(curr_key, "get")
    if full_list_ob_objects:
        for elem in full_list_ob_objects:
            validator_petstore.validate_request_schema(curr_key, elem, "get")
    assert True


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_assert_all_random_is_valid_request_put_v_24(curr_key):
    full_list_ob_objects = petstore_generator.get_all_possible_request_objects(curr_key, "put")
    if full_list_ob_objects:
        for elem in full_list_ob_objects:
            validator_petstore.validate_request_schema(curr_key, elem, "put")
    assert True


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_assert_all_random_is_valid_request_delete_v_24(curr_key):
    full_list_ob_objects = petstore_generator.get_all_possible_request_objects(curr_key, "delete")
    if full_list_ob_objects:
        for elem in full_list_ob_objects:
            validator_petstore.validate_request_schema(curr_key, elem, "delete")
    assert True


# ****************** RESPONSE ******************** #

# ~~~~~~ REQUIRE ~~~~ #

@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_assert_require_is_valid_response_post_v_24(curr_key):
    object_to_test = petstore_generator.get_required_response_object(curr_key, "post")
    validator_petstore.validate_response_schema(curr_key, object_to_test, "post")
    assert True


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_assert_require_is_valid_response_put_v_24(curr_key):
    object_to_test = petstore_generator.get_required_response_object(curr_key, "put")
    validator_petstore.validate_response_schema(curr_key, object_to_test, "put")
    assert True


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_assert_require_is_valid_response_get_v_24(curr_key):
    object_to_test = petstore_generator.get_required_response_object(curr_key, "get")
    validator_petstore.validate_response_schema(curr_key, object_to_test, "get")
    assert True


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_assert_require_is_valid_response_delete_v_24(curr_key):
    object_to_test = petstore_generator.get_required_response_object(curr_key, "delete")
    validator_petstore.validate_response_schema(curr_key, object_to_test, "delete")
    assert True


# ~~~~~~ FULL ~~~~ #


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_assert_full_is_valid_response_post_v_24(curr_key):
    object_to_test = petstore_generator.get_full_response_object(curr_key, "post")
    validator_petstore.validate_response_schema(curr_key, object_to_test, "post")
    assert True


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_assert_require_is_valid_response_put_v_24(curr_key):
    object_to_test = petstore_generator.get_full_response_object(curr_key, "put")
    validator_petstore.validate_response_schema(curr_key, object_to_test, "put")
    assert True


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_assert_require_is_valid_response_get_v_24(curr_key):
    object_to_test = petstore_generator.get_full_response_object(curr_key, "get")
    validator_petstore.validate_response_schema(curr_key, object_to_test, "get")
    assert True


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_assert_require_is_valid_response_delete_v_24(curr_key):
    object_to_test = petstore_generator.get_full_response_object(curr_key, "delete")
    validator_petstore.validate_response_schema(curr_key, object_to_test, "delete")
    assert True


# ~~~~~~ RANDOM  ~~~~ #

@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_assert_all_random_is_valid_response_post_v_24(curr_key):
    full_list_ob_objects = petstore_generator.get_all_possible_response_objects(curr_key, 'post')
    if full_list_ob_objects:
        for elem in full_list_ob_objects:
            assert validator_petstore.validate_response_schema(curr_key, elem, "post")
    assert True


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_assert_all_random_is_valid_response_get_v_24(curr_key):
    full_list_ob_objects = petstore_generator.get_all_possible_response_objects(curr_key, "get")
    if full_list_ob_objects:
        for elem in full_list_ob_objects:
            assert validator_petstore.validate_response_schema(curr_key, elem, "get")
    assert True


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_assert_all_random_is_valid_response_put_v_24(curr_key):
    full_list_ob_objects = petstore_generator.get_all_possible_response_objects(curr_key, "put")
    if full_list_ob_objects:
        for elem in full_list_ob_objects:
            assert validator_petstore.validate_response_schema(curr_key, elem, "put")
    assert True


@pytest.mark.parametrize("curr_key", list(petstore_schemas.keys()))
def test_assert_all_random_is_valid_response_delete_v_24(curr_key):
    full_list_ob_objects = petstore_generator.get_all_possible_response_objects(curr_key, "delete")
    if full_list_ob_objects:
        for elem in full_list_ob_objects:
            assert validator_petstore.validate_response_schema(curr_key, elem, "delete")
    assert True


# *********************** TEST ALL FUNCTIONALITY OF METHODS ************************ #

# *********************** DATA MANAGEMENT ************************ #

# ~~~~~~ REQUIRE ~~~~ #
request_endpoint = "/exec/stored"
request_field = "name"


def test_get_require_data():
    data = jobs_generator.get_required_request_object(request_endpoint)
    assert validator_jobs.validate_request_schema(request_endpoint, data)


def test_get_require_data_with_change():
    data = jobs_generator.get_required_request_object(request_endpoint, change={request_field: new_value})
    assert data[request_field] == new_value


def test_get_require_data_with_add():
    data = jobs_generator.get_required_request_object(request_endpoint, add={new_field: new_value})
    assert data[new_field] == new_value


def test_get_require_data_with_remove():
    data = jobs_generator.get_required_request_object(request_endpoint, remove={request_field})
    assert request_field not in data


def test_require_other_require_request_not_interfere_from_change():
    jobs_generator.get_required_request_object(request_endpoint, change={request_field: new_value})
    data = jobs_generator.get_required_request_object(request_endpoint)
    assert data[request_field] != new_value


def test_full_other_require_request_not_interfere_from_change():
    jobs_generator.get_full_request_object(request_endpoint, change={request_field: new_value})
    data = jobs_generator.get_required_request_object(request_endpoint)
    assert data[request_field] != new_value


def test_min_val_other_require_request_not_interfere_from_change():
    jobs_generator.get_min_val_request_object(request_endpoint, change={request_field: new_value})
    data = jobs_generator.get_required_request_object(request_endpoint)
    assert data[request_field] != new_value


def test_random_other_require_request_not_interfere_from_change():
    jobs_generator.get_random_request_object(request_endpoint, change={request_field: new_value})
    data = jobs_generator.get_required_request_object(request_endpoint)
    assert data[request_field] != new_value


# ~~~~~~ FULL ~~~~ #


def test_get_full_data():
    data = jobs_generator.get_full_request_object(request_endpoint)
    assert validator_jobs.validate_request_schema(request_endpoint, data)


def test_get_full_data_with_change():
    data = jobs_generator.get_full_request_object(request_endpoint, change={request_field: new_value})
    assert data[request_field] == new_value


def test_get_full_data_with_add():
    data = jobs_generator.get_full_request_object(request_endpoint, add={new_field: new_value})
    assert data[new_field] == new_value


def test_get_full_data_with_remove():
    data = jobs_generator.get_full_request_object(request_endpoint, remove={request_field})
    assert request_field not in data


def test_require_other_full_request_not_interfere_from_change():
    jobs_generator.get_required_request_object(request_endpoint, change={request_field: new_value})
    data = jobs_generator.get_full_request_object(request_endpoint)
    assert data[request_field] != new_value


def test_full_other_full_request_not_interfere_from_change():
    jobs_generator.get_full_request_object(request_endpoint, change={request_field: new_value})
    data = jobs_generator.get_full_request_object(request_endpoint)
    assert data[request_field] != new_value


def test_min_val_other_full_request_not_interfere_from_change():
    jobs_generator.get_min_val_request_object(request_endpoint, change={request_field: new_value})
    data = jobs_generator.get_full_request_object(request_endpoint)
    assert data[request_field] != new_value


def test_random_other_full_request_not_interfere_from_change():
    jobs_generator.get_random_request_object(request_endpoint, change={request_field: new_value})
    data = jobs_generator.get_full_request_object(request_endpoint)
    assert data[request_field] != new_value


# ~~~~~~ MIN VAL ~~~~ #


def test_get_min_val_data():
    data = jobs_generator.get_min_val_request_object(request_endpoint)
    assert validator_jobs.validate_request_schema(request_endpoint, data)


def test_get_min_val_data_with_change():
    data = jobs_generator.get_min_val_request_object(request_endpoint, change={request_field: new_value})
    assert data[request_field] == new_value


def test_get_min_val_data_with_add():
    data = jobs_generator.get_min_val_request_object(request_endpoint, add={new_field: new_value})
    assert data[new_field] == new_value


def test_get_min_val_data_with_remove():
    data = jobs_generator.get_min_val_request_object(request_endpoint, remove={request_field})
    assert request_field not in data


def test_require_other_min_val_request_not_interfere_from_change():
    jobs_generator.get_required_request_object(request_endpoint, change={request_field: new_value})
    data = jobs_generator.get_min_val_request_object(request_endpoint)
    assert data[request_field] != new_value


def test_full_other_min_val_request_not_interfere_from_change():
    jobs_generator.get_full_request_object(request_endpoint, change={request_field: new_value})
    data = jobs_generator.get_min_val_request_object(request_endpoint)
    assert data[request_field] != new_value


def test_min_val_other_min_val_request_not_interfere_from_change():
    jobs_generator.get_min_val_request_object(request_endpoint, change={request_field: new_value})
    data = jobs_generator.get_min_val_request_object(request_endpoint)
    assert data[request_field] != new_value


def test_random_other_min_val_request_not_interfere_from_change():
    jobs_generator.get_random_request_object(request_endpoint, change={request_field: new_value})
    data = jobs_generator.get_min_val_request_object(request_endpoint)
    assert data[request_field] != new_value


# ~~~~~~ RANDOM ~~~~~ #


def test_get_random_data_with_change():
    data = jobs_generator.get_random_request_object(request_endpoint, change={request_field: new_value})
    assert data[request_field] == new_value


def test_get_random_data_with_add():
    data = jobs_generator.get_random_request_object(request_endpoint, add={new_field: new_value})
    assert data[new_field] == new_value


def test_get_random_data_with_remove():
    data = jobs_generator.get_random_request_object(request_endpoint, remove={request_field})
    assert request_field not in data


def test_require_other_random_request_not_interfere_from_change():
    jobs_generator.get_required_request_object(request_endpoint, change={request_field: new_value})
    data = jobs_generator.get_random_request_object(request_endpoint)
    assert data[request_field] != new_value


def test_full_other_random_request_not_interfere_from_change():
    jobs_generator.get_full_request_object(request_endpoint, change={request_field: new_value})
    data = jobs_generator.get_random_request_object(request_endpoint)
    assert data[request_field] != new_value


def test_min_val_other_random_request_not_interfere_from_change():
    jobs_generator.get_min_val_request_object(request_endpoint, change={request_field: new_value})
    data = jobs_generator.get_random_request_object(request_endpoint)
    assert data[request_field] != new_value


def test_random_other_random_request_not_interfere_from_change():
    jobs_generator.get_random_request_object(request_endpoint, change={request_field: new_value})
    data = jobs_generator.get_random_request_object(request_endpoint)
    assert data[request_field] != new_value


# ~~~~ SET DEFAULT VALUES ~~~~ #

def test_set_changes_gets_all():
    data = jobs_generator.set_default_request_values(request_endpoint, change={request_field: new_value})
    assert validator_jobs.validate_request_schema(request_endpoint, data)

    data = jobs_generator.get_required_request_object(request_endpoint)
    assert data[request_field] == new_value

    data = jobs_generator.get_full_request_object(request_endpoint)
    assert data[request_field] == new_value

    data = jobs_generator.get_min_val_request_object(request_endpoint)
    assert data[request_field] == new_value

    data = jobs_generator.get_random_request_object(request_endpoint)
    assert data[request_field] == new_value


# *********************** RESPONSE ************************ #

# ~~~~ REQUIRE ~~~~ #

response_endpoint = "/cron/results/{name}"
response_field = 'jobId'


def test_get_require_data_response():
    data = jobs_generator.get_required_response_object(response_endpoint)
    if len(data) > 0:
        assert validator_jobs.validate_response_schema(response_endpoint, data)
    else:
        assert True


def test_get_require_data_with_change_response():
    data = jobs_generator.get_required_response_object(response_endpoint, change={response_field: new_value})
    if len(data) > 0:
        assert data[0][response_field] == new_value
    else:
        assert True


def test_get_require_data_with_add_response():
    data = jobs_generator.get_required_response_object(response_endpoint, add={new_field: new_value})
    if len(data) > 0:
        assert data[0][response_field] != new_value
    else:
        assert True


def test_get_require_data_with_remove_response():
    data = jobs_generator.get_required_response_object(response_endpoint, remove={response_field})
    if len(data) > 0:
        assert response_field not in data[0]
    else:
        assert True


def test_require_other_require_request_not_interfere_from_change_response():
    jobs_generator.get_required_response_object(response_endpoint, change={response_field: new_value})
    data = jobs_generator.get_required_response_object(response_endpoint)
    if len(data) > 0:
        assert data[0][response_field] != new_value
    else:
        assert True


def test_full_other_require_request_not_interfere_from_change_response():
    jobs_generator.get_full_response_object(response_endpoint, change={response_field: new_value})
    data = jobs_generator.get_required_response_object(response_endpoint)
    if len(data) > 0:
        assert data[0][response_field] != new_value
    else:
        assert True


def test_min_val_other_require_request_not_interfere_from_change_response():
    jobs_generator.get_min_val_response_object(response_endpoint, change={response_field: new_value})
    data = jobs_generator.get_required_response_object(response_endpoint)
    if len(data) > 0:
        assert data[0][response_field] != new_value
    else:
        assert True


def test_random_other_require_request_not_interfere_from_change_response():
    jobs_generator.get_random_response_object(response_endpoint, change={response_field: new_value})
    data = jobs_generator.get_required_response_object(response_endpoint)
    if len(data) > 0:
        assert data[0][response_field] != new_value
    else:
        assert True


# ~~~~ FULL ~~~~ #

def test_get_full_data_response():
    data = jobs_generator.get_full_response_object(response_endpoint)
    if len(data) > 0:
        assert validator_jobs.validate_response_schema(response_endpoint, data)
    else:
        assert True


def test_get_full_data_with_change_response():
    data = jobs_generator.get_full_response_object(response_endpoint, change={response_field: new_value})
    if len(data) > 0:
        assert data[0][response_field] == new_value
    else:
        assert True


def test_get_full_data_with_add_response():
    data = jobs_generator.get_full_response_object(response_endpoint, add={new_field: new_value})
    if len(data) > 0:
        assert data[0][response_field] != new_value
    else:
        assert True


def test_get_full_data_with_remove_response():
    data = jobs_generator.get_full_response_object(response_endpoint, remove={response_field})
    if len(data) > 0:
        assert response_field not in data[0]
    else:
        assert True


def test_require_other_full_request_not_interfere_from_change_response():
    jobs_generator.get_required_response_object(response_endpoint, change={response_field: new_value})
    data = jobs_generator.get_full_response_object(response_endpoint)
    if len(data) > 0:
        assert data[0][response_field] != new_value
    else:
        assert True


def test_full_other_full_request_not_interfere_from_change_response():
    jobs_generator.get_full_response_object(response_endpoint, change={response_field: new_value})
    data = jobs_generator.get_full_response_object(response_endpoint)
    if len(data) > 0:
        assert data[0][response_field] != new_value
    else:
        assert True


def test_min_val_other_full_request_not_interfere_from_change_response():
    jobs_generator.get_min_val_response_object(response_endpoint, change={response_field: new_value})
    data = jobs_generator.get_full_response_object(response_endpoint)
    if len(data) > 0:
        assert data[0][response_field] != new_value
    else:
        assert True


def test_random_other_full_request_not_interfere_from_change_response():
    jobs_generator.get_random_response_object(response_endpoint, change={response_field: new_value})
    data = jobs_generator.get_full_response_object(response_endpoint)
    if len(data) > 0:
        assert data[0][response_field] != new_value
    else:
        assert True


# ~~~~ MIN VAL ~~~~ #

def test_get_min_val_data_response():
    data = jobs_generator.get_min_val_response_object(response_endpoint)
    if len(data) > 0:
        assert validator_jobs.validate_response_schema(response_endpoint, data)
    else:
        assert True


def test_get_min_val_data_with_change_response():
    data = jobs_generator.get_min_val_response_object(response_endpoint, change={response_field: new_value})
    if len(data) > 0:
        assert data[0][response_field] == new_value
    else:
        assert True


def test_get_min_val_data_with_add_response():
    data = jobs_generator.get_min_val_response_object(response_endpoint, add={new_field: new_value})
    if len(data) > 0:
        assert data[0][response_field] != new_value
    else:
        assert True


def test_get_min_val_data_with_remove_response():
    data = jobs_generator.get_min_val_response_object(response_endpoint, remove={response_field})
    if len(data) > 0:
        assert response_field not in data[0]
    else:
        assert True


def test_require_other_min_val_request_not_interfere_from_change_response():
    jobs_generator.get_required_response_object(response_endpoint, change={response_field: new_value})
    data = jobs_generator.get_min_val_response_object(response_endpoint)
    if len(data) > 0:
        assert data[0][response_field] != new_value
    else:
        assert True


def test_full_other_min_val_request_not_interfere_from_change_response():
    jobs_generator.get_full_response_object(response_endpoint, change={response_field: new_value})
    data = jobs_generator.get_min_val_response_object(response_endpoint)
    if len(data) > 0:
        assert data[0][response_field] != new_value
    else:
        assert True


def test_min_val_other_min_val_request_not_interfere_from_change_response():
    jobs_generator.get_min_val_response_object(response_endpoint, change={response_field: new_value})
    data = jobs_generator.get_min_val_response_object(response_endpoint)
    if len(data) > 0:
        assert data[0][response_field] != new_value
    else:
        assert True


def test_random_other_min_val_request_not_interfere_from_change_response():
    jobs_generator.get_random_response_object(response_endpoint, change={response_field: new_value})
    data = jobs_generator.get_min_val_response_object(response_endpoint)
    if len(data) > 0:
        assert data[0][response_field] != new_value
    else:
        assert True


# ~~~~ RANDOM ~~~~ #

def test_get_random_data_with_change_response():
    data = jobs_generator.get_random_response_object(response_endpoint, change={response_field: new_value})
    if len(data) > 0:
        assert data[0][response_field] == new_value
    else:
        assert True


def test_get_random_data_with_add_response():
    data = jobs_generator.get_random_response_object(response_endpoint, add={new_field: new_value})
    if len(data) > 0:
        assert data[0][response_field] != new_value
    else:
        assert True


def test_get_random_data_with_remove_response():
    data = jobs_generator.get_random_response_object(response_endpoint, remove={response_field})
    if len(data) > 0:
        assert response_field not in data[0]
    else:
        assert True


def test_require_other_random_request_not_interfere_from_change_response():
    jobs_generator.get_required_response_object(response_endpoint, change={response_field: new_value})
    data = jobs_generator.get_random_response_object(response_endpoint)
    if len(data) > 0:
        assert data[0][response_field] != new_value
    else:
        assert True


def test_full_other_random_request_not_interfere_from_change_response():
    jobs_generator.get_full_response_object(response_endpoint, change={response_field: new_value})
    data = jobs_generator.get_random_response_object(response_endpoint)
    if len(data) > 0:
        assert data[0][response_field] != new_value
    else:
        assert True


def test_min_val_other_random_request_not_interfere_from_change_response():
    jobs_generator.get_min_val_response_object(response_endpoint, change={response_field: new_value})
    data = jobs_generator.get_random_response_object(response_endpoint)
    if len(data) > 0:
        assert data[0][response_field] != new_value
    else:
        assert True


def test_random_other_random_request_not_interfere_from_change_response():
    jobs_generator.get_random_response_object(response_endpoint, change={response_field: new_value})
    data = jobs_generator.get_random_response_object(response_endpoint)
    if len(data) > 0:
        assert data[0][response_field] != new_value
    else:
        assert True


# ~~~~ SET DEFAULT VALUES ~~~~ #


def test_set_changes_gets_require_response():
    data = jobs_generator.set_default_response_values(response_endpoint, change={response_field: new_value})
    if len(data) > 0:
        assert validator_jobs.validate_response_schema(response_endpoint, data)
    else:
        assert True

    data = jobs_generator.get_required_response_object(response_endpoint)
    if len(data) > 0:
        assert data[0][response_field]
    else:
        assert True

    data = jobs_generator.get_full_response_object(response_endpoint)
    if len(data) > 0:
        assert data[0][response_field]
    else:
        assert True

    data = jobs_generator.get_random_response_object(response_endpoint)
    if len(data) > 0:
        assert data[0][response_field]
    else:
        assert True
