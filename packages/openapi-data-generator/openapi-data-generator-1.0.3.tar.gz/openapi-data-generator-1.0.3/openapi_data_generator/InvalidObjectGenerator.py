from copy import deepcopy
from .utils import filter_to_require_keys, remove_keys_from_data, get_all_levels_keys, \
    split_key_and_delimiters_to_list, get_keys_and_attr
from compare_objects import compare_objects

# ************************** GET LIST OF WRONG TYPES ********************** #

# ALL WRONG TYPES
# BELOW MINIMUM (STR / NUMBER)
# ABOVE MAX (STR / NUMBER)
# ARR WITH MIN_ITEMS
# ARR WITH UNIQUE ITEMS
# All NONE-REQUIRED FIELDS

incorrect_values_by_type = {'string': "--- wrong_value ---", 'num': 1, 'boolean': True, 'null': None, 'array': [],
                            'object': {}}
ls_of_types = ['string', 'num', 'boolean', 'null', 'array', 'object']


def append_to_list(ret_ls: list, info: str, object_to_add):
    ret_ls.append({'info': info, 'data': object_to_add})


def string(*args):
    ret_ls = []
    if "enum" in args[0].keys():
        ret_ls.append("--- Out Of Enum ---")
    if "pattern" in args[0].keys():
        ret_ls.append("--- Out Of pattern ---")
    if "minLength" in args[0].keys() and args[0]['minLength'] > 0:
        ret_ls.append("-" * (int(args[0]['minLength']) - 1))
    if "maxLength" in args[0].keys():
        ret_ls.append(
            "-" * int(int(args[0]['maxLength'] / 2)) + "  Long string " + "-" * int(int(args[0]['maxLength']) / 2))
    return ret_ls


def num(*args):
    ret_ls = []
    if "minimum" in args[0].keys():
        min_edge = args[0]["minimum"]
        if "exclusiveMinimum" in args[0].keys() and \
                (args[0]["exclusiveMinimum"] or args[0]["exclusiveMinimum"] == min_edge):
            min_edge += 1
        ret_ls.append(int(min_edge) - 10)
    if "maximum" in args[0].keys():
        max_edge = args[0]["maximum"]
        if "exclusiveMaximum" in args[0].keys() and \
                (args[0]["exclusiveMaximum"] or args[0]["exclusiveMaximum"] == max_edge):
            max_edge -= 1
        ret_ls.append(int(max_edge) + 10)
    return ret_ls


def boolean(*args):
    ret_ls = []
    return ret_ls


def null(*args):
    ret_ls = []
    return ret_ls


def array(*args):
    ret_ls = []
    attr, key, object_to_scan = args
    ls_of_items = get_list_of_items(key, object_to_scan)
    if isinstance(ls_of_items, list):
        if 'minItems' in attr.keys() and attr['minItems'] > 0:
            ret_ls.append(deepcopy(ls_of_items)[:attr['minItems'] - 1])
        if 'maxItems' in attr.keys() and len(ls_of_items) > 0:
            ret_ls.append(deepcopy(ls_of_items) + (deepcopy(ls_of_items[:1]) * attr['maxItems']))
        if 'uniqueItems' in attr.keys() and len(ls_of_items) > 0:
            ret_ls.append(deepcopy(ls_of_items) + deepcopy(ls_of_items[:1]))
    return ret_ls


def object_(*args):
    ret_ls = []
    return ret_ls


function_of_wrong_types = {'string': string, 'number': num, 'integer': num, 'boolean': boolean, 'null': null,
                           'array': array, 'object': object_}


def get_list_of_items(key, object_to_scan):
    key_list = split_key_and_delimiters_to_list(key)
    if isinstance(object_to_scan, list):
        object_to_scan = object_to_scan[0]
    for i in range(0, len(key_list) - 2, 2):
        if key_list[i + 1] == ":":
            object_to_scan = object_to_scan[key_list[i]]
        else:
            if object_to_scan[key_list[i]] is None:
                return []
            object_to_scan = object_to_scan[key_list[i]][0]

    return object_to_scan[key_list[-1]]


def get_list_of_wrong_types(attr_types):
    attr_types = [elem if elem not in ['number', 'integer'] else 'num' for elem in attr_types]
    relevant_list = list(set(ls_of_types) - set(attr_types))
    res = [incorrect_values_by_type[curr_type] for curr_type in relevant_list]
    return res


def get_wrong_values(key, attr, object_to_scan, is_nested=False):
    if ("oneOf" in attr.keys() or 'anyOf' in attr.keys()) and 'type' not in attr.keys():
        rel_key = 'oneOf' if "oneOf" in attr.keys() else 'anyOf'
        sum_ls = []
        ls_of_possible_types = []
        for curr_attr in attr[rel_key]:
            sum_ls += get_wrong_values(key, curr_attr, object_to_scan, True)
            ls_of_possible_types.append(curr_attr['type'] if curr_attr['type'] not in ['number', 'integer'] else 'num')
        return sum_ls + get_list_of_wrong_types(ls_of_possible_types)
    else:
        return handle_attribute(attr, is_nested, key, object_to_scan)


def is_array(key, object_to_scan):
    cp = deepcopy(object_to_scan)
    key_list = split_key_and_delimiters_to_list(key)
    for i in range(0, len(key_list) - 2, 2):
        if key_list[i] in cp:
            if key_list[i + 1] == ":":
                cp = cp[key_list[i]]
            else:
                ls = cp[key_list[i]] if cp[key_list[i]] else []
                if len(ls) > 0:
                    cp = cp[key_list[i]][0]
                else:
                    return False
        else:
            return False
    if key_list[-1] in cp.keys():
        return isinstance(cp[key_list[-1]], list)
    return False


def handle_attribute(attr, is_nested, key, object_to_scan):
    ret_ls = []
    if 'type' in attr.keys():
        curr_types = [attr['type']]
        if 'nullable' in attr.keys() and attr['nullable']:
            curr_types += ["null"]
        if isinstance(object_to_scan, dict) and is_array(key, object_to_scan) and 'array' not in attr['type']:
            curr_types += ['array']
        if not is_nested:
            ret_ls += get_list_of_wrong_types(curr_types)
        for curr_type in curr_types:
            ret_ls += function_of_wrong_types[curr_type](attr, key, object_to_scan)

    return ret_ls


# ************************ GET MISSING REQUIRE OBJECTS ************************* #


def get_list_of_missing_require_fields(schema, object_to_scan, list_of_keys):
    ret_ls = []
    require_keys = filter_to_require_keys(schema, list_of_keys)
    for key in require_keys:
        append_to_list(ret_ls, f"{key} is required", remove_keys_from_data(object_to_scan, [key], from_invalid=True))
    return ret_ls


# ******************************* Set in object ************************* #

def add_invalid_additional_properties(attr, object_to_scan, ret_ls, key):
    if "additionalProperties" in attr.keys() and attr["additionalProperties"] is False:
        wrong_data = deepcopy(object_to_scan)
        ref_to_base = wrong_data
        if isinstance(wrong_data, list):
            wrong_data = wrong_data[0]
        key_list = split_key_and_delimiters_to_list(key)
        handle_additional_properties(key, key_list, object_to_scan, ref_to_base, ret_ls, wrong_data)


def handle_additional_properties(key, key_list, object_to_scan, ref_to_base, ret_ls, wrong_data):
    if len(key) > 1:
        for i in range(0, len(key_list) - 2, 2):
            if key_list[i + 1] == ":":
                wrong_data = wrong_data[key_list[i]]
            else:
                if wrong_data[key_list[i]] is None:
                    wrong_data[key_list[i]] = {}
                    return
                elif len(wrong_data[key_list[i]]) > 0:
                    wrong_data = wrong_data[key_list[i]][0]
    set_wrong_additional_property(key_list, object_to_scan, ref_to_base, ret_ls, wrong_data)


def set_wrong_additional_property(key_list, object_to_scan, ref_to_base, ret_ls, wrong_data):
    if key_list[-1] in wrong_data.keys() and wrong_data[key_list[-1]]:
        if isinstance(wrong_data[key_list[-1]], list):
            if len(wrong_data[key_list[-1]]):
                wrong_data[key_list[-1]][0].update({"---- additional property ----": 1})
            else:
                return
        else:
            wrong_data[key_list[-1]].update({"---- additional property ----": 1})
        if not compare_objects(ref_to_base, object_to_scan):
            append_to_list(ret_ls, f"Set additional property to '{key_list[-1]}'", ref_to_base)


def loop_over_key_list_and_set_wrong_val(already_sets, key_list, refer_to_object, res_ls, wrong_value):
    for i in range(0, len(key_list) - 2, 2):
        if key_list[i + 1] == "-":
            ls = refer_to_object.get(key_list[i], [])
            ls = ls if ls else []
            for j in range(len(ls)):
                set_wrong_val_in_key("".join(key_list[i + 2:]), wrong_value, refer_to_object[key_list[i]][j], res_ls)
                already_sets = True
        else:
            if isinstance(refer_to_object, dict) and key_list[i] in refer_to_object.keys():
                refer_to_object = refer_to_object[key_list[i]]
    return already_sets, refer_to_object


def set_wrong_val_in_key(key, wrong_value, object_to_scan, res_ls, is_root=False):
    key_list = split_key_and_delimiters_to_list(key)
    refer_to_object = object_to_scan
    already_sets = False
    if isinstance(refer_to_object, list):
        refer_to_object = refer_to_object[0]
    already_sets, refer_to_object = loop_over_key_list_and_set_wrong_val(already_sets, key_list, refer_to_object,
                                                                         res_ls, wrong_value)
    if not already_sets:
        refer_to_object[key_list[-1]] = wrong_value
    if is_root:
        append_to_list(res_ls, f"`{wrong_value}` is wrong value for '{key}'", object_to_scan)


def get_invalid_object_refer_single_key(key, attr, object_to_scan):
    ret_ls = []
    wrong_values = get_wrong_values(key, attr, object_to_scan)
    for wrong_value in wrong_values:
        set_wrong_val_in_key(key, wrong_value, deepcopy(object_to_scan), ret_ls, True)
    add_invalid_additional_properties(attr, object_to_scan, ret_ls, key)
    return ret_ls


# ******************************* main ************************* #


def get_ls_of_invalid_objects(object_to_scan: object or list, schema: dict) -> list:
    object_to_scan_, schema_ = deepcopy(object_to_scan), deepcopy(schema)
    ls_of_objects = []

    # generate_all_keys
    keys = get_all_levels_keys(object_to_scan_)
    key_and_attr = get_keys_and_attr(schema_, keys)

    # create list without required fields
    mis_require_ls = get_list_of_missing_require_fields(schema_, object_to_scan_, keys)

    # create list without with wrong values
    for pair in key_and_attr:
        ls_of_objects += get_invalid_object_refer_single_key(pair[0], pair[1], object_to_scan_)

    # combine them together both and return
    return ls_of_objects + mis_require_ls

