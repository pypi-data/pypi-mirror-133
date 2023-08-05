
import re

# ************************ SLICE AND COMBINE_KEYS ******************** #


def step_into_dict(key):
    return f"{key}:"


def step_into_list(key):
    return f"{key}-"


def is_last_key(key):
    return len(key) == 1


def value_is_dict(key):
    return ":" in key[1]


def value_is_list(key):
    return "-" in key[1]


def first_key(key):
    return key[0]


def get_curr_and_rest_of_keys(curr_key):
    delimiter_index_dict = None
    delimiter_index_list = None
    if ":" in curr_key:
        delimiter_index_dict = curr_key.index(":")
    if "-" in curr_key:
        delimiter_index_list = curr_key.index("-")
    if not delimiter_index_dict and not delimiter_index_list:
        return curr_key, ""

    if delimiter_index_list and delimiter_index_dict:
        delimiter = ":" if delimiter_index_dict < delimiter_index_list else "-"
    else:
        delimiter = ":" if delimiter_index_dict else "-"
    return curr_key[:curr_key.index(delimiter)], curr_key[curr_key.index(delimiter) + 1:]


def fuse_key_list(key_list: list, index=0) -> str:
    return "".join(key_list[index:])


def fuse_key_list_from_start(key_list: list, index=0) -> str:
    return "".join(key_list[:index])


def merge_lists(keys, delimiters):
    j = 1
    for delimiter in delimiters:
        keys.insert(j, delimiter)
        j += 2
    return keys


def split_key_and_delimiters_to_list(key: str) -> list:
    delimiters = [c for c in key if c == "-" or c == ":"]
    keys = []
    temp = key.split(":")
    for i in temp:
        keys += i.split("-")
    return merge_lists(keys, delimiters)


def get_curr_object_from_key(key):
    last_key_without_delimiter = re.findall(r"[\w']+", key)
    return last_key_without_delimiter[-1]

# ************************ RECOGNIZE KEYS FROM OBJECT ******************** #

def dive_into_object(add_pre_obj, key, ls_of_keys, result, value):
    if isinstance(value, dict):
        result += get_all_leaf_keys(value, f"{add_pre_obj}{key}:")
    elif isinstance(value, list):
        for elem in value:
            if isinstance(elem, dict):
                result += get_all_leaf_keys(elem, f"{add_pre_obj}{key}-")
    if len(result) != 0:
        ls_of_keys += result
    else:
        ls_of_keys.append(f"{add_pre_obj}{key}")
    return ls_of_keys


def get_all_leaf_keys(object_to_scan, add_pre_obj=''):
    ls_of_keys = []
    if isinstance(object_to_scan, list):
        if len(object_to_scan) == 0:
            return ls_of_keys
        object_to_scan = object_to_scan[0]
    if not isinstance(object_to_scan, dict):
        return ls_of_keys
    for key, value in object_to_scan.items():
        result = []
        ls_of_keys = dive_into_object(add_pre_obj, key, ls_of_keys, result, value)
    return sorted(list(set(ls_of_keys)))


def get_possible_keys(key_list):
    ret_ls = []
    while len(key_list) > 0:
        ret_ls.append("".join(key_list))
        key_list = key_list[:-2]
    return ret_ls


def add_middle_keys(keys):
    ret_ls = []
    if not keys:
        return ret_ls
    for key in keys:
        ret_ls += get_possible_keys(split_key_and_delimiters_to_list(key))
    return list(set(ret_ls))


def get_all_levels_keys(object_to_scan):
    return add_middle_keys(get_all_leaf_keys(object_to_scan))

