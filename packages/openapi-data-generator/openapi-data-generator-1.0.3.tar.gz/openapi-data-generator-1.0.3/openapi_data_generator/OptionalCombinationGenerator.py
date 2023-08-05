# ********************** generate_all_possible_object ******************************* #
#                                                                                     #
#   generate_all_possible_object -                                                    #
#                                                                                     #
#       Description:                                                                  #
#                                                                                     #
#           This util is useful to find all optional differences between              #
#           sub-dictionary, to complete one - and generate all option of              #
#           object by their properties                                                #
#                                                                                     #
#                                                                                     #
# *********************************************************************************** #
from copy import deepcopy
from .utils import get_all_leaf_keys, object_in_list, filter_to_require_keys, get_curr_and_rest_of_keys, \
    step_into_dict, get_all_levels_keys, remove_keys_from_data


# ~~~~~ COMPLETE MISSING FULLY REQUIRE SUB OBJECTS  ~~~~~~~~~~ #


def get_relevant_key_single_dict(req_obj, diff_keys, base_key):
    req_obj_keys_level = req_obj.keys()
    ret_ls = []
    for i in range(len(diff_keys)):
        root_key, rest_of_keys = get_curr_and_rest_of_keys(diff_keys[i])
        if root_key not in req_obj_keys_level:
            ret_ls.append(f"{base_key}{root_key}")
        elif isinstance(req_obj[root_key], dict):
            ret_ls += get_optional_fully_require_keys(req_obj[root_key], [rest_of_keys],
                                                      step_into_dict(base_key + root_key))
    return list(set(ret_ls))


def get_optional_fully_require_keys(req_obj, diff_keys, base_key=""):
    if isinstance(req_obj, dict):
        return get_relevant_key_single_dict(req_obj, diff_keys, base_key)
    if isinstance(req_obj, list):
        ret_ls = []
        for elem in req_obj:
            ret_ls += get_relevant_key_single_dict(elem, diff_keys, base_key)
        return list(set(ret_ls))


# ~~~~~ UPDATE FOR NEW FULLY REQUIRE DATA ~~~~~~~~~~ #


def get_missing_fully_require_data(req_obj, fully_required, schema):
    # get difference between required and full required
    diff_keys = difference_between_two_objects(fully_required, req_obj)
    # extract from key the root keys and not the leafs
    relevant_keys = get_optional_fully_require_keys(req_obj, diff_keys)
    # create all range of objects
    keys_combinations = get_all_permutations(relevant_keys)
    return get_all_objects(fully_required, req_obj, keys_combinations, schema, True)


def get_full_required_object(schema, req_obj, full_obj):
    #  remove from them the keys of required object
    diff_keys = list(set(get_all_levels_keys(full_obj)) - set(get_all_levels_keys(req_obj)))
    # filter to require_keys
    diff_keys = filter_to_require_keys(schema, diff_keys)
    # create dictionary from keys
    return get_dict_from_combination(tuple(diff_keys), full_obj, req_obj, schema)


def update_in_case_of_schema(schema, diff_keys, req_obj, full_obj):
    if len(diff_keys) == 0:
        return diff_keys, req_obj, []
    if schema:
        fully_require = get_full_required_object(schema, req_obj, full_obj)
        missing_data = get_missing_fully_require_data(req_obj, fully_require, schema)
        diff_keys = list(
            set(get_all_leaf_keys(full_obj)) - set(get_all_leaf_keys(fully_require)))
        return diff_keys, fully_require, missing_data
    return diff_keys, req_obj, []


# *********************** CREATE DIFF KEYS ************************* #


def difference_between_two_objects(full, require):
    return list(set(get_all_leaf_keys(full)) - set(get_all_leaf_keys(require)))


def get_diff_keys(req_obj, full_obj):
    return difference_between_two_objects(full_obj, req_obj)


# *********************** CREATE PERMUTATIONS ************************* #

def get_all_permutations(list_to_perm):
    import itertools
    ret_ls = []
    if len(list_to_perm) == 0:
        return []
    if len(list_to_perm) == 1:
        return list(itertools.combinations(list_to_perm, 1))
    for i in range(1, len(list_to_perm) + 1):
        temp_ls = list(itertools.combinations(list_to_perm, i))
        for val in temp_ls:
            ret_ls.append(val)
    return ret_ls


# **************** CREATE LIST OF RELEVANT OBJECTS ****************** #


def get_dict_from_combination(key_combination, full_obj, req_obj, schema, add_nested_full_require=False):
    diff = list(set(get_all_leaf_keys(full_obj)) - set(get_all_leaf_keys(req_obj)))
    non_comb_keys = list(set(diff) - set(key_combination))
    if schema and add_nested_full_require:
        nested_require_keys = set(filter_to_require_keys(schema, get_all_leaf_keys(full_obj))) - set(
            get_all_leaf_keys(req_obj))
        non_comb_keys = list(set(non_comb_keys) - nested_require_keys)
    new_data = remove_keys_from_data(full_obj, non_comb_keys, schema)
    return new_data


def get_all_objects(full_obj, req_obj, keys_combinations, schema, add_nested_full_require=False):
    ret_ls = []
    for key_combination in keys_combinations:
        ret_ls.append(get_dict_from_combination(key_combination, full_obj, req_obj, schema, add_nested_full_require))
    return ret_ls


# *********************** MAIN FUNCTION ************************* #


def parse_and_generate(req_obj: dict or list, full_obj: dict or list, schema: dict) -> list:
    # protection from invalid objects
    if not req_obj or not full_obj:
        return []
    if isinstance(req_obj, list) and isinstance(full_obj, list) and (len(req_obj) == 0 or len(full_obj) == 0):
        return []

    diff_keys = get_diff_keys(req_obj, full_obj)

    # In case it has schema we do 3 things:
    #   1. refactor require to full require ( include inside nested optional data)
    #   2. edit diff keys list
    #   3. add missing list of data (without optional keys)
    diff_keys, req_obj, missing_data = update_in_case_of_schema(schema, diff_keys, req_obj, full_obj)

    keys_combinations = get_all_permutations(diff_keys)
    return get_all_objects(full_obj, req_obj, keys_combinations, schema) + missing_data


def generate_all_possible_objects(req_obj, full_obj, schema=None):
    req_obj_, full_obj_, schema_ = deepcopy(req_obj), deepcopy(full_obj), deepcopy(schema)
    ret_list = []
    if req_obj_ and full_obj_:
        ret_list = parse_and_generate(req_obj_, full_obj_, schema_)
    if not object_in_list(full_obj_, ret_list):
        ret_list += [full_obj_]
    if not object_in_list(req_obj_, ret_list):
        ret_list.insert(0, req_obj_)
    return ret_list
