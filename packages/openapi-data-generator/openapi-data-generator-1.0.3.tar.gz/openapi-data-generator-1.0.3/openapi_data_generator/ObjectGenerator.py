# system imports
from random import randint, choice, uniform
from datetime import datetime
from copy import deepcopy
import rstr
import string
import os
import time
import uuid
import base64
import json

# project imports
from compare_objects import compare_objects
from .InvalidObjectGenerator import get_ls_of_invalid_objects
from .OptionalCombinationGenerator import generate_all_possible_objects


class ObjectsGenerator(object):
    _file_cache_names = ['require', 'full', 'edge', 'possibilities', 'invalid']

    def __init__(self, schema, config, generate_invalid=False, cache_dir="", cache_pack={}):
        self.schema = schema
        self.chances_queue = []
        self.non_require_is_empty = False
        self.config = config
        self._gen_invalid = generate_invalid
        self.dict_of_types = {"string": self.get_string, "number": self.get_number, "integer": self.get_integer,
                              "boolean": self.get_boolean, "null": self.get_null, "array": self.get_array,
                              "object": self.get_object}

        if cache_dir != "":
            self.__using_cache(cache_dir, cache_pack)
        else:
            self.__set_all_objects()

    def __using_cache(self, cache_dir, cache_pack):
        title, endpoint, method = [cache_pack.get(key) for key in ["title", 'endpoint', 'method']]
        full_path = f"{cache_dir}/objects/{title}/{endpoint.replace('/', '_')}/{method}"

        if 'res_num' in cache_pack:
            full_path += f"/{cache_pack['res_num']}"
        if os.path.isdir(full_path):
            self.required_object = self.read_json(f"{full_path}/require.json")
            self.full_object = self.read_json(f"{full_path}/full.json")
            self.min_val_object = self.read_json(f"{full_path}/edge.json")
            self.all_possible_objects = self.read_json(f"{full_path}/possibilities.json")

            if self._gen_invalid:
                if len(self.read_json(f"{full_path}/invalid.json")) == 0:
                    self.invalid_objects = get_ls_of_invalid_objects(self.full_object, self.schema)
                    self.write_json(f"{full_path}/invalid.json", self.invalid_objects)
                else:
                    self.invalid_objects = self.read_json(f"{full_path}/invalid.json")
            else:
                self.invalid_objects = []
                self.write_json(f"{full_path}/invalid.json", self.invalid_objects)

        else:
            self.__set_all_objects()
            os.makedirs(full_path)
            objects = [self.required_object, self.full_object, self.min_val_object, self.all_possible_objects,
                       self.invalid_objects]
            [self.write_json(f"{full_path}/{self._file_cache_names[i]}.json", objects[i]) for i in range(len(objects))]

    def __set_all_objects(self):
        if self.schema:
            self.full_object = self.create_object(required_only=False)
            self.required_object = self.create_object(required_only=True)
            self.min_val_object = self.create_object(min_val_object=True)
            self.invalid_objects = get_ls_of_invalid_objects(self.full_object, self.schema) if self._gen_invalid else []
            self.all_possible_objects = generate_all_possible_objects(self.required_object, self.full_object,
                                                                      self.schema)
        else:
            self.full_object = self.required_object = self.min_val_object = None
            self.all_possible_objects = []
            self.invalid_objects = []

    def create_object(self, required_only=False, min_val_object=False):
        schema_ = deepcopy(self.schema)
        return self.extract_from_schema_and_parse(schema_, required_only, min_val_object)

    def get_correct_type(self, attribute, schema, required_only, min_val_object):
        curr_type = attribute["type"]
        return self.dict_of_types[curr_type](attribute, schema, required_only, min_val_object)

    def get_value(self, attribute, schema, required_only, min_val_object):
        if "type" in attribute:
            return self.get_correct_type(attribute, schema, required_only, min_val_object)
        if "properties" in attribute:
            return self.extract_from_schema_and_parse(attribute, required_only, min_val_object)
        if "$ref" in attribute:
            return self.extract_from_schema_and_parse(self.schema[attribute["$ref"].split("/")[1]], required_only,
                                                      min_val_object)
        if "oneOf" in attribute or "anyOf" in attribute:
            rel_key = "oneOf" if "oneOf" in attribute else 'anyOf'
            list_of_options = attribute[rel_key]
            return self.get_value(list_of_options[randint(0, len(list_of_options) - 1)], schema, required_only,
                                  min_val_object)

    def extract_from_schema_and_parse(self, schema, required_only, min_val_object):
        return self.parse_data_by_properties(schema, required_only, min_val_object)

    def parse_data_by_properties(self, schema, required_only, min_val_object):
        builtin_object = {}
        if "oneOf" in schema or "anyOf" in schema:
            rel_key = "oneOf" if "oneOf" in schema else 'anyOf'
            return self.get_value(schema[rel_key][randint(0, len(schema[rel_key]) - 1)], schema, required_only,
                                  min_val_object)
        if "properties" in schema:
            self.scan_properties(builtin_object, required_only, schema, min_val_object)
        else:
            return self.get_value(schema, schema, required_only, min_val_object)
        return builtin_object

    def scan_properties(self, builtin_object, required_only, schema, min_val_object):
        fields_to_get = list(schema["properties"].keys())
        if required_only:
            if "required" in schema:
                fields_to_get = schema["required"]
            elif self.non_require_is_empty:
                fields_to_get = []
        for key, value in schema["properties"].items():
            if key in fields_to_get:
                builtin_object.update({key: self.get_value(value, schema, required_only, min_val_object)})

    # ******************** VALUE GETTERS ************************ #

    # attribute, schema, required_only, min_val_object
    def get_string(self, *args):
        if 'default' in args[0] and randint(1, self.config['default_probability'] + 1) == 1:
            return args[0]['default']
        if 'nullable' in args[0] and randint(1, self.config['nullable_probability'] + 1) == 1:
            return None
        if "enum" in args[0]:
            return args[0]["enum"][randint(0, len(args[0]["enum"])) - 1]

        if "pattern" in args[0]:
            return rstr.xeger(args[0]['pattern'])
        min_len = args[0].get('minLength', self.config['min_str_len'])
        max_len = args[0].get('maxLength', self.config['max_str_len'])
        if "format" in args[0]:
            val = ObjectsGenerator.get_string_format(args[0]["format"], min_len, max_len)
            if val != 'Default Format string':
                return val
        if args[3]:
            max_len = min_len
        return self.get_random_string(min_len, max_len)

    # attribute, schema, required_only, min_val_object
    def get_number(self, *args):
        edges = {'min': self.config['min_float'], 'max': self.config['max_float']}
        if 'default' in args[0] and randint(1, self.config['default_probability'] + 1) == 1:
            return args[0]['default']
        if 'nullable' in args[0] and randint(1, self.config['nullable_probability'] + 1) == 1:
            return None
        if "enum" in args[0]:
            return args[0]["enum"][randint(0, len(args[0]["enum"])) - 1]
        if "format" in args[0]:
            res = self.get_number_format(args[0]['format'], edges)
            if res:
                return res
        self.__get_min_and_max(args, edges)
        if args[3]:
            return float(max(0, edges['min']))
        if 'multipleOf' in args[0]:
            return choice([num for num in range(edges['min'], edges['max']) if num % args[0]['multipleOf'] == 0])
        return uniform(edges['min'], edges['max'])

    # attribute, schema, required_only, min_val_object
    def get_integer(self, *args):
        edges = {'min': self.config['min_int'], 'max': self.config['max_int']}
        if 'default' in args[0] and randint(1, self.config['default_probability'] + 1) == 1:
            return args[0]['default']
        if 'nullable' in args[0] and randint(1, self.config['nullable_probability'] + 1) == 1:
            return None
        if "enum" in args[0]:
            return args[0]["enum"][randint(0, len(args[0]["enum"])) - 1]
        if "format" in args[0]:
            res = self.get_number_format(args[0]['format'], edges)
            if res:
                return int(res)
        self.__get_min_and_max(args, edges)
        if args[3]:
            return max(0, edges['min'])
        if 'multipleOf' in args[0]:
            return choice([num for num in range(edges['min'], edges['max']) if num % args[0]['multipleOf'] == 0])
        return randint(edges['min'], edges['max'])

    @staticmethod
    def __get_min_and_max(args, edges):
        if "minimum" in args[0]:
            edges['min'] = args[0]["minimum"]
            if "exclusiveMinimum" in args[0] and \
                    (args[0]["exclusiveMinimum"] or args[0]["exclusiveMinimum"] == edges['min']):
                edges['min'] += 1
            edges['max'] = edges['max'] if edges['max'] > edges['min'] else edges['min']
        if "maximum" in args[0]:
            edges['max'] = args[0]["maximum"]
            if "exclusiveMaximum" in args[0] and \
                    (args[0]["exclusiveMaximum"] or args[0]["exclusiveMaximum"] == edges['max']):
                edges['max'] -= 1
            edges['min'] = edges['min'] if edges['min'] < edges['max'] else edges['max']

    def get_boolean(self, *args):
        if 'default' in args[0] and randint(1, self.config['default_probability'] + 1) == 1:
            return args[0]['default']
        if 'nullable' in args[0] and randint(1, self.config['nullable_probability'] + 1) == 1:
            return None
        return not not randint(0, 1)

    def get_null(self, *args):
        if 'default' in args[0] and randint(1, self.config['default_probability'] + 1) == 1:
            return args[0]['default']
        return None

    def get_edges(self, attribute):
        min_edge = self.config['array_min_items']
        max_edge = self.config['array_max_items']
        if "minItems" in attribute:
            min_edge = attribute["minItems"]
        if "maxItems" in attribute:
            max_edge = attribute["maxItems"]
        return min_edge, max_edge

    # attribute, schema, required_only, min_val_object
    def get_array(self, *args):
        if 'default' in args[0] and randint(1, self.config['default_probability'] + 1) == 1:
            return args[0]['default']
        if 'nullable' in args[0] and randint(1, self.config['nullable_probability'] + 1) == 1:
            return None
        attribute = args[0]
        if ("oneOf" in attribute or 'anyOf' in attribute) and "items" in attribute:
            rel_key = 'oneOf' if "oneOf" in attribute else 'anyOf'
            attribute.update(args[0][rel_key][randint(0, len(args[0][rel_key]) - 1)])
        elif "oneOf" in attribute or 'anyOf' in attribute:
            rel_key = 'oneOf' if "oneOf" in attribute else 'anyOf'
            attribute = args[0][rel_key][randint(0, len(args[0][rel_key]) - 1)]
        elif "items" not in attribute:
            return []
        min_edge, max_edge = self.get_edges(attribute)
        return self.generate_array((attribute, args[1], args[2], args[3]), min_edge, max_edge)

    def generate_array(self, args, min_edge, max_edge):
        ret_array = []
        if args[3]:
            array_length = min_edge
        else:
            array_length = randint(min_edge, max_edge)
        for _ in range(array_length):
            generated_value = self.get_value(args[0]["items"], args[1], args[2], args[3])
            if "uniqueItems" in args[0] and args[0]["uniqueItems"] is True:
                while self.value_already_in_list(ret_array, generated_value) is True:
                    generated_value = self.get_value(args[0]["items"], args[1], args[2], args[3])
            ret_array.append(generated_value)
        return ret_array

    # attribute, schema, required_only, min_val_object
    def get_object(self, *args):
        if 'default' in args[0] and randint(1, self.config['default_probability'] + 1) == 1:
            return args[0]['default']
        if 'nullable' in args[0] and randint(1, self.config['nullable_probability'] + 1) == 1:
            return None
        if "properties" not in args[0]:
            return {}
        if "type" in args[0] and "properties" in args[0]:
            return self.parse_data_by_properties(args[0], args[2], args[3])
        return self.extract_from_schema_and_parse(args[0], args[2], args[3])

    # ******************** CHANGE FIELD VALUE ************************ #

    def change_values(self, change=None, required_object=True):
        key_errors = []
        if isinstance(change, dict):
            for key, value in change.items():
                object_to_scan = self.required_object if required_object else self.full_object
                change = self.set_single_value(object_to_scan, key, value)
                if change is False:
                    key_errors.append(key)

    @staticmethod
    def value_already_in_list(list_of_val, val):
        for ls_val in list_of_val:
            if isinstance(val, dict):
                if compare_objects(ls_val, val) is True:
                    return True
            else:
                if ls_val == val:
                    return True
        return False

    @staticmethod
    def get_string_format(requested_format, min_edge, max_edge):
        full_date = str(datetime.now().isoformat())
        if requested_format == "date-time":
            return full_date
        elif requested_format == "date":
            return full_date.split('T')[0]
        elif requested_format == "time":
            return full_date.split('T')[1]
        elif requested_format == 'uuid':
            return str(uuid.UUID(int=randint(0, 65535)))
        elif requested_format == "byte":
            rand_string = ObjectsGenerator.get_random_string(min_edge, max_edge)
            message_bytes = rand_string.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)
            return base64_bytes.decode('ascii')
        elif requested_format == "binary":
            rand_string = ObjectsGenerator.get_random_string(min_edge, max_edge)
            message_bytes = rand_string.encode('utf-8')
            base64_bytes = base64.b64encode(message_bytes)
            return base64_bytes.decode('utf-8')
        elif requested_format == "ipv4":
            return rstr.xeger(r"^[1-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$")
        elif requested_format == 'email':
            return f"{ObjectsGenerator.get_random_string(min_edge, max_edge)}@example.com"
        elif requested_format == 'hostname':
            return f'www.{ObjectsGenerator.get_random_string(min_edge, max_edge)}.com'
        elif requested_format == 'json-pointer' or requested_format == 'relative-json-format':
            return f'{ObjectsGenerator.get_random_string(min_edge, max_edge)}/' \
                   f'{ObjectsGenerator.get_random_string(min_edge, max_edge)}/' \
                   f'{ObjectsGenerator.get_random_string(min_edge, max_edge)}'
        else:
            return 'Default Format string'

    @staticmethod
    def get_number_format(requested_format, edges):
        if requested_format == "int8":
            edges['min'] = -128
            edges['max'] = 127
        if requested_format == "int16":
            edges['min'] = -32768
            edges['max'] = 32767
        elif requested_format == "int32":
            edges['min'] = -2147483648
            edges['max'] = 2147483647
        elif requested_format == "int64":
            edges['min'] = -9223372036854775808
            edges['max'] = 9223372036854775807
        elif requested_format == "uint8":
            edges['min'] = 0
            edges['max'] = 255
        elif requested_format == "uint16":
            edges['min'] = 0
            edges['max'] = 65535
        elif requested_format == "uint32":
            edges['min'] = 0
            edges['max'] = 4294967295
        elif requested_format == "uint64":
            edges['min'] = 0
            edges['max'] = 18446744073709551615
        elif requested_format == "float":
            edges['min'] = 3.4 * pow(10, -38)
            edges['max'] = 3.4 * pow(10, 38)
        elif requested_format == "double":
            edges['min'] = 1.7 * pow(10, -308)
            edges['max'] = 1.7 * pow(10, -308)
        elif requested_format == "time":
            return time.time()

    @staticmethod
    def get_random_string(min_length, max_length):
        letters = string.ascii_letters
        length = randint(min_length, max_length)
        return ''.join(choice(letters) for _ in range(length))

    @staticmethod
    def set_specific_value(key, requested_key, requested_value, value, object_to_scan):
        if key == requested_key:
            object_to_scan[key] = requested_value
            return True
        if isinstance(value, dict) and ObjectsGenerator.set_single_value(value, requested_key, requested_value):
            return True
        if isinstance(value, list):
            for i in value:
                if isinstance(i, dict) and ObjectsGenerator.set_single_value(i, requested_key, requested_value):
                    return True
        return False

    @staticmethod
    def set_single_value(object_to_scan, requested_key, requested_value):
        ret = False
        if isinstance(object_to_scan, dict):
            for key, value in object_to_scan.items():
                ret = ObjectsGenerator.set_specific_value(key, requested_key, requested_value, value, object_to_scan)
                if ret is True:
                    break
        return ret

    @staticmethod
    def write_json(path, data):
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def read_json(path):
        with open(path) as f:
            return json.load(f)

