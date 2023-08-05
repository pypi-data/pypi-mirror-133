from .KeysHandler import split_key_and_delimiters_to_list, get_curr_object_from_key


# ************************* GET ATTR BY KEY ************************* #


def get_curr_component(root_schema, curr_component, node, key):
    if curr_component:
        if "properties" not in curr_component.keys():
            return curr_component
        attribute = curr_component['properties'][node] if "properties" in curr_component.keys() else curr_component
        if "$ref" in attribute.keys():
            return root_schema[attribute['$ref'][2:]]
        if "items" in attribute.keys():
            if "$ref" in attribute['items'].keys():
                return root_schema[attribute['items']['$ref'][2:]]
            elif "-" in key:
                return attribute['items']
        return attribute


def get_leaf_component(root_schema, curr_component, node):
    if curr_component:
        if "properties" not in curr_component.keys():
            return curr_component
        attribute = curr_component['properties'][node] if "properties" in curr_component.keys() else curr_component
        if "$ref" in attribute.keys():
            return root_schema[attribute['$ref'][2:]]
        return attribute


def get_component_schema(schema, key):
    key_list = split_key_and_delimiters_to_list(key)
    root_schema = schema
    curr_component = get_root_schema(root_schema)
    for i in range(0, len(key_list) - 2, 2):
        curr_component = get_curr_component(root_schema, curr_component, key_list[i], key)
    return curr_component


def get_main_object(root_schema):
    if '$ref' in root_schema['items'].keys():
        return root_schema[root_schema['items']['$ref'][2:]]
    else:
        return root_schema['items']


def get_root_schema(root_schema):
    if 'type' in root_schema.keys() and root_schema['type'] == 'array':
        main_object = get_main_object(root_schema)
        root_schema.update(main_object)
        root_schema.pop("items")
    return root_schema


def get_attr(schema, key):
    key_list = split_key_and_delimiters_to_list(key)
    root_schema = schema
    curr_component = get_root_schema(root_schema)
    for i in range(0, len(key_list) - 2, 2):
        curr_component = get_curr_component(root_schema, curr_component, key_list[i], key)
    return get_leaf_component(root_schema, curr_component, key_list[-1])


def get_keys_and_attr(schema: dict, keys: list) -> list:
    ret_ls = []
    for i in range(len(keys)):
        attr = get_attr(schema, keys[i])
        ret_ls.append([keys[i], attr])
    return ret_ls


def is_key_require_in_nested(schema, key):
    key_list = split_key_and_delimiters_to_list(key)
    root_schema = schema
    curr_component = get_root_schema(root_schema)
    for i in range(0, len(key_list) - 2, 2):
        curr_component = get_curr_component(root_schema, curr_component, key_list[i], key)
    curr_key_to_test_if_require = get_curr_object_from_key(key)
    if isinstance(curr_component, dict) and "required" in curr_component.keys():
        return curr_key_to_test_if_require in curr_component['required']
    return False


def filter_to_require_keys(schema, keys):
    ret_ls = []
    for key in keys:
        if is_key_require_in_nested(schema, key):
            ret_ls.append(key)
    return ret_ls
