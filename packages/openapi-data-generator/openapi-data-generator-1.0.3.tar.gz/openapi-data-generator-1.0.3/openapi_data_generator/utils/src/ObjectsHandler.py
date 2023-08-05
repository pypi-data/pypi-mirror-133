from copy import deepcopy
from .KeysHandler import split_key_and_delimiters_to_list, fuse_key_list, get_all_levels_keys, get_all_leaf_keys
from .SchemaHandler import get_component_schema
from compare_objects import compare_objects


def obj_in_ls(ob, ls):
    for elem in ls:
        if compare_objects(elem, ob):
            return True
    return False


def ensure_unique(ls: list):
    # return new list with unique items
    new_ls = []
    for elem in ls:
        if not obj_in_ls(elem, new_ls):
            new_ls.append(elem)
    return new_ls


def remove_from_single_object(runner, key, full_key_track, schema, from_invalid):
    key_list = split_key_and_delimiters_to_list(key)

    if len(key_list) == 1 and key_list[-1] in runner:
        # if is require key - do not pop this key out
        if schema:
            curr_comp = get_component_schema(schema, full_key_track)
            if not ("required" in curr_comp and key_list[-1] in curr_comp['required']):
                runner.pop(key_list[-1])
        else:
            runner.pop(key_list[-1])
    else:
        # proceed to final key
        recursive_keep_search(full_key_track, key_list, runner, schema, from_invalid)


def handle_unique_items(curr_key, full_key_track, runner, schema):
    # if schema and array contains unique items - ensure it unique
    if schema:
        curr_full_key = "".join(full_key_track.split(curr_key)[0]) + curr_key
        curr_comp = get_component_schema(schema, curr_full_key)
        if "properties" in curr_comp and "uniqueItems" in curr_comp['properties'][curr_key] and \
                curr_comp['properties'][curr_key]['uniqueItems']:
            runner[curr_key] = ensure_unique(runner[curr_key])


def is_suit_object(elem, curr_key):
    elem_keys = get_all_leaf_keys(elem)
    return curr_key in elem_keys


def recursive_keep_search(full_key_track, key_list, runner, schema, from_invalid):
    for i in range(0, len(key_list) - 2, 2):
        curr_key = key_list[i]
        if curr_key in runner and runner[curr_key] is not None:
            if key_list[i + 1] == "-":
                for elem in runner[curr_key]:
                    # in case of list of items and are change one each other - change key for correct object
                    if is_suit_object(elem, fuse_key_list(key_list, i + 2)) or from_invalid:
                        remove_from_single_object(elem, fuse_key_list(key_list, i + 2), full_key_track, schema,
                                                  from_invalid)
                handle_unique_items(curr_key, full_key_track, runner, schema)
                break
            else:
                runner = runner[curr_key]
                if is_suit_object(runner, fuse_key_list(key_list, i + 2)) or from_invalid:
                    remove_from_single_object(runner, fuse_key_list(key_list, i + 2), full_key_track, schema,
                                              from_invalid)
                break


def remove_keys_from_data(object_to_scan, keys, schema=None, from_invalid=False):
    runner = deepcopy(object_to_scan)
    base = runner
    for key in keys:
        if isinstance(runner, list):
            for elem in runner:
                remove_from_single_object(elem, key, key, schema, from_invalid)
        else:
            remove_from_single_object(runner, key, key, schema, from_invalid)
    return base


# check if object is in list

def compare_object_keys(a, b):
    return sorted(get_all_levels_keys(a)) == sorted(get_all_levels_keys(b))


def object_in_list(single_object, ret_list):
    if not isinstance(single_object, dict) or isinstance(single_object, list):
        return single_object in ret_list
    for elem in ret_list:
        if compare_object_keys(elem, single_object):
            return True
    return False
