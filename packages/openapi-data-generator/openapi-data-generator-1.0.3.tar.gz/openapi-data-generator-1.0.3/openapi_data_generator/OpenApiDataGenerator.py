from .ObjectGenerator import ObjectsGenerator
from openapi_schema_generator import OpenApiSchemaGenerator
from .utils import LockDirectory
from copy import deepcopy
from random import randint
import os
import shutil
import textwrap


class OpenApiDataGenerator(object):
    __settings = {'default_probability': 5, 'nullable_probability': 5, 'array_min_items': 0, 'array_max_items': 5,
                  'min_str_len': 1, 'max_str_len': 10, 'min_int': -2147483648, 'max_int': 2147483647,
                  'min_float': 3.4 * pow(10, -38), 'max_float': 3.4 * pow(10, 38)}

    def __init__(self, path, generate_responses=False, generate_invalid=False, use_cache=False, restart_cache=False):
        self.__path = path
        self.__schemas = None
        self.__response_gen = generate_responses
        self.__use_cache = use_cache
        self.__restart_cache = restart_cache
        self.__generate_invalid = generate_invalid
        self.__config = deepcopy(self.__settings)
        self.__cache_dir = ""
        self.__dir_locker = LockDirectory(".api_gen_cache")
        self.regenerate()

    # ********************** API ****************** #

    def keys(self):
        return self.__schemas.keys()

    def regenerate(self, restart_cache=False):
        restart_cache = restart_cache if restart_cache else self.__restart_cache
        if self.__use_cache or restart_cache:
            self.__create_cache_dir(self.__path)
            with self.__dir_locker:
                if restart_cache:
                    self.__restart_cache_dir(self.__path)
                self.__generate()
        else:
            self.__generate()

    def __generate(self):
        if self.__use_cache:
            full_path = f"{self.__cache_dir}/schemas.json"
            if os.path.isdir(self.__cache_dir) and os.path.isfile(full_path):
                self.__schemas = ObjectsGenerator.read_json(full_path)
            else:
                self.__schemas = OpenApiSchemaGenerator(self.__path).build_mapped_schema()
                ObjectsGenerator.write_json(full_path, self.__schemas)
        else:
            self.__schemas = OpenApiSchemaGenerator(self.__path).build_mapped_schema()
        self.__set_objects()

    def __repr__(self):
        ret_string = "\n\n*********************   DATA DETAILS     ********************\n\n"
        for key_to_endpoint, value in self.objects.items():
            ret_string += f"\n~~~~~~~~~~~ Endpoint  --> {key_to_endpoint} : ~~~~~~~~~~~ \n"
            ret_string += f"Contain data for {list(value.keys())} methods\n\n"
            for method in value.keys():
                if self.__response_gen and 'requestBody' in value[method].keys():
                    ret_string += "\n\n^^^^^^^^^^^^^^^^^   Request objects    ^^^^^^^^^^^^^^^\n\n"
                ret_string += self.__get_request_string(key_to_endpoint, method)
                if self.__response_gen and 'responses' in value[method].keys():
                    ret_string += "\n\n^^^^^^^^^^^^^^^^^   Response objects    ^^^^^^^^^^^^^^^"
                    for status_code in value[method]['responses'].keys():
                        ret_string += f"\n\n^^^^^^^^^^^^^^^^^   Status Code {status_code}    ^^^^^^^^^^^^^^^\n\n"
                        ret_string += self.__get_response_string(key_to_endpoint, method, status_code)

        return ret_string

    @staticmethod
    def set_general_behavior(array_min_items: int = None, array_max_items: int = None, default_probability: int = None,
                             nullable_probability: int = None, max_str_length: int = None, min_int=None, max_int=None,
                             min_float=None, max_float=None):
        OpenApiDataGenerator.__set_values_in_settings(OpenApiDataGenerator.__settings, **locals())
        for key, value in locals().items():
            if value:
                OpenApiDataGenerator.__settings[key] = value

    def set_instance_behavior(self, array_min_items: int = None, array_max_items: int = None,
                              default_probability: int = None,
                              nullable_probability: int = None, max_str_length: int = None, min_int=None, max_int=None,
                              min_float=None, max_float=None):
        locals().pop('self')
        self.__set_values_in_settings(self.__config, **locals())
        self.regenerate(restart_cache=self.__restart_cache)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     REQUEST BODY    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    # ************** SERVICE FUNCTIONS **************** #

    def __get_request_object(self, endpoint, method):
        if method.lower() in self.objects[endpoint].keys() and \
                "requestBody" in self.objects[endpoint][method.lower()].keys():
            return self.objects[endpoint][method.lower()]["requestBody"]

    def __get_possibility_request_list(self, endpoint, method):
        curr_object = self.__get_request_object(endpoint, method)
        if curr_object:
            return curr_object.all_possible_objects
        return []

    # ************** REQUIRE **************** #

    def get_required_request_object(self, endpoint, method="post", change={}, add={}, remove={}):
        curr_object = self.__get_request_object(endpoint, method)
        return self.__fetch_data(deepcopy(curr_object), change, add, remove, required_object=True)

    # ************** FULL **************** #

    def get_full_request_object(self, endpoint, method="post", change={}, add={}, remove={}):
        curr_object = self.__get_request_object(endpoint, method)
        return self.__fetch_data(deepcopy(curr_object), change, add, remove)

    # ************** RANDOM **************** #

    def get_random_request_object(self, endpoint, method="post", change={}, add={}, remove={}):
        possible_ls = self.__get_possibility_request_list(endpoint, method)
        if len(possible_ls) > 0:
            return self.__edit_dict(deepcopy(possible_ls[randint(0, len(possible_ls) - 1)]), change, add, remove)

    # ************** EDGE **************** #

    def get_min_val_request_object(self, endpoint, method="post", change={}, add={}, remove={}):
        curr_object = self.__get_request_object(endpoint, method)
        return self.__fetch_data(deepcopy(curr_object), change, add, remove, min_val_object=True)

    # ************** ALL LIST **************** #

    def get_all_possible_request_objects(self, endpoint, method="post"):
        return self.__get_possibility_request_list(endpoint, method)

    # ************** INVALID **************** #

    def get_invalid_request_object(self, endpoint, method="post", with_info=False):
        if self.__generate_invalid:
            curr_object = self.__get_request_object(endpoint, method)
            if curr_object and len(curr_object.invalid_objects) > 0:
                invalid_obj_ls = self.__fetch_invalid_object_ls(curr_object.invalid_objects, with_info)
                return invalid_obj_ls[randint(0, len(invalid_obj_ls)) - 1]
        return []

    # ************** LIST INVALID **************** #

    def get_all_invalid_request_objects(self, endpoint, method="post", with_info=False):
        if self.__generate_invalid:
            curr_object = self.__get_request_object(endpoint, method)
            if curr_object:
                return self.__fetch_invalid_object_ls(curr_object.invalid_objects, with_info)
        return []

    # ************** GET LIST OF RANDOM **************** #

    def get_list_of_random_request_data(self, endpoint, method="post", length=100, full_object=True, change={}, add={},
                                        remove={}):
        return [
            self.__fetch_data(self.__generate_request_object(endpoint, method), change, add, remove, not full_object)
            for _ in range(length)]

    # ************** SET DEFAULT **************** #

    def set_default_request_values(self, endpoint, method="post", change={}, add={}, remove={}):
        general_object = self.__get_request_object(endpoint, method)

        # set base objects
        general_object.required_object = self.__fetch_data(general_object, change, add, remove, required_object=True)
        general_object.full_object = self.__fetch_data(general_object, change, add, remove)
        general_object.min_val_object = self.__fetch_data(general_object, change, add, remove, min_val_object=True)

        # change possible list
        option_list = self.__get_possibility_request_list(endpoint, method)
        for i in range(len(option_list)):
            option_list[i] = self.__edit_dict(option_list[i], change, add, remove)
        return general_object.required_object

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     RESPONSES    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    # ************** SERVICE FUNCTIONS **************** #

    def __get_response_object(self, endpoint, method, response_num):
        method = method.lower()
        if method in self.objects[endpoint] and \
                "responses" in self.objects[endpoint][method] and \
                str(response_num) in self.objects[endpoint][method]["responses"]:
            return self.objects[endpoint][method]["responses"][str(response_num)]

    def __get_possibility_response_list(self, endpoint, method, response_num):
        curr_object = self.__get_response_object(endpoint, method, response_num)
        if curr_object:
            return curr_object.all_possible_objects
        return []

    # ************** REQUIRE **************** #

    def get_required_response_object(self, endpoint, method="get", response_num=200, change={}, add={}, remove={}):
        data = self.__get_response_object(endpoint, method, response_num)
        if data:
            return self.__fetch_data(deepcopy(data), change, add, remove, required_object=True)

    # ************** FULL **************** #

    def get_full_response_object(self, endpoint, method="get", response_num=200, change={}, add={}, remove={}):
        data = self.__get_response_object(endpoint, method, response_num)
        if data:
            return self.__fetch_data(deepcopy(data), change, add, remove)

    # ************** RANDOM **************** #

    def get_random_response_object(self, endpoint, method="get", response_num=200, change={}, add={}, remove={}):
        possible_ls = self.__get_possibility_response_list(endpoint, method, response_num)
        if len(possible_ls) > 0:
            return self.__edit_dict(deepcopy(possible_ls[randint(0, len(possible_ls) - 1)]), change, add, remove)

    # ************** EDGE **************** #

    def get_min_val_response_object(self, endpoint, method="get", response_num=200, change={}, add={}, remove={}):
        curr_object = self.__get_response_object(endpoint, method, response_num)
        return self.__fetch_data(deepcopy(curr_object), change, add, remove, min_val_object=True)

    # ************** FULL LIST **************** #

    def get_all_possible_response_objects(self, endpoint, method="get", response_num=200):
        return self.__get_possibility_response_list(endpoint, method, response_num)

    # ************** INVALID **************** #

    def get_invalid_response_object(self, endpoint, method="get", response_num=200, with_info=False):
        if self.__generate_invalid and self.__response_gen:
            curr_object = self.__get_response_object(endpoint, method, response_num)
            if curr_object and len(curr_object.invalid_objects) > 0:
                invalid_obj_ls = self.__fetch_invalid_object_ls(curr_object.invalid_objects, with_info)
                return invalid_obj_ls[randint(0, len(invalid_obj_ls)) - 1]

    # ************** LIST INVALID **************** #

    def get_all_invalid_response_objects(self, endpoint, method="get", response_num=200, with_info=False):
        if self.__generate_invalid and self.__response_gen:
            curr_object = self.__get_response_object(endpoint, method, response_num)
            if curr_object:
                return self.__fetch_invalid_object_ls(curr_object.invalid_objects, with_info)

    # ************** GET LIST OF RANDOM **************** #

    def get_list_of_random_response_data(self, endpoint, method="get", res_num=200, length=100, full_object=True,
                                         change={}, add={}, remove={}):
        return [self.__fetch_data(self.__generate_response_object(endpoint, method, res_num), change, add, remove,
                                  not full_object) for _ in range(length)]

    # ************** SET DEFAULT **************** #

    def set_default_response_values(self, endpoint, method="get", response_num=200, change={}, add={}, remove={}):
        if not self.__response_gen:
            return None
        general_object = self.__get_response_object(endpoint, method, response_num)
        general_object.required_object = self.__fetch_data(general_object, change, add, remove, required_object=True)
        general_object.full_object = self.__fetch_data(general_object, change, add, remove)
        general_object.min_val_object = self.__fetch_data(general_object, change, add, remove, min_val_object=True)

        option_list = self.__get_possibility_response_list(endpoint, method, response_num)
        for i in range(len(option_list)):
            option_list[i] = self.__edit_dict(option_list[i], change, add, remove)
        return general_object.required_object

    # ************************ SERVICE FUNCTIONS ****************************************** #

    # ************** HANDLE CACHE DIR **************** #

    def __get_cache_dir(self, path):
        slash = "/"
        rel_path = os.path.abspath(path).replace("\\", slash)
        file_name = rel_path.split(slash)[-1].split(".")[0]
        self.__cache_dir = f".api_gen_cache/{file_name}"

    def __restart_cache_dir(self, path):
        self.__get_cache_dir(path)
        if os.path.isdir(self.__cache_dir):
            shutil.rmtree(self.__cache_dir)
            os.makedirs(self.__cache_dir)

    def __create_cache_dir(self, path):
        self.__get_cache_dir(path)
        try:
            if not os.path.isdir(self.__cache_dir):
                os.makedirs(self.__cache_dir)
        except FileExistsError:
            pass

    # ************** FETCH STR TO __repr__ **************** #

    def __get_request_string(self, key_to_object, method):
        string_to_print = ""
        prefix_width = 80
        indent = '\t'
        if self.get_required_request_object(key_to_object, method):
            base_prefix = f"--- Data for Rest type for `{method}`:  ---\n\n"
            prefix = "- Require Object : \n"
            wrapper = textwrap.TextWrapper(initial_indent=indent, width=prefix_width,
                                           subsequent_indent=indent)
            message = f"\n{self.get_required_request_object(key_to_object, method)}"
            string_to_print += base_prefix + prefix + wrapper.fill(message) + "\n\n"

            prefix = "- Full Object : \n"
            wrapper = textwrap.TextWrapper(initial_indent=indent, width=prefix_width,
                                           subsequent_indent=indent)
            message = f"\n{self.get_full_request_object(key_to_object, method)}"
            string_to_print += prefix + wrapper.fill(message) + "\n\n"

            possibility_len = len(self.get_all_possible_request_objects(key_to_object, method))
            prefix = f"- Length of possibilities is {possibility_len}; Example :\n"
            wrapper = textwrap.TextWrapper(initial_indent=indent, width=prefix_width,
                                           subsequent_indent=indent)
            message = f"\n{self.get_random_request_object(key_to_object, method)}"
            string_to_print += prefix + wrapper.fill(message) + "\n\n"

            possibility_len = len(self.get_all_invalid_request_objects(key_to_object, method))
            prefix = f"- Length of invalid is {possibility_len}; Example :\n"
            wrapper = textwrap.TextWrapper(initial_indent=indent, width=prefix_width,
                                           subsequent_indent=indent)
            message = f"\n{self.get_invalid_request_object(key_to_object, method)}"
            string_to_print += prefix + wrapper.fill(message) + "\n"
        return string_to_print + "\n\n" if string_to_print != "" else ""

    def __get_response_string(self, key_to_object, method, status_code):
        string_to_print = ""
        prefix_width = 80
        indent = '\t'
        if self.get_required_response_object(key_to_object, method, status_code):
            base_prefix = f"--- Data for Rest type for `{method}`:  ---\n\n"
            prefix = "- Require Object : \n"
            wrapper = textwrap.TextWrapper(initial_indent=indent, width=prefix_width,
                                           subsequent_indent=indent)
            message = f"\n{self.get_required_response_object(key_to_object, method, status_code)}"
            string_to_print += base_prefix + prefix + wrapper.fill(message) + "\n\n"

            prefix = "- Full Object : \n"
            wrapper = textwrap.TextWrapper(initial_indent=indent, width=prefix_width,
                                           subsequent_indent=indent)
            message = f"\n{self.get_full_response_object(key_to_object, method, status_code)}"
            string_to_print += prefix + wrapper.fill(message) + "\n\n"

            possibility_len = len(self.get_all_possible_response_objects(key_to_object, method, status_code))
            prefix = f"- Length of possibilities is {possibility_len}; Example :\n"
            wrapper = textwrap.TextWrapper(initial_indent=indent, width=prefix_width,
                                           subsequent_indent=indent)
            message = f"\n{self.get_random_response_object(key_to_object, method, status_code)}"
            string_to_print += prefix + wrapper.fill(message) + "\n\n"

            possibility_len = len(self.get_all_invalid_response_objects(key_to_object, method, status_code))
            prefix = f"- Length of invalid is {possibility_len}; Example :\n"
            wrapper = textwrap.TextWrapper(initial_indent=indent, width=prefix_width,
                                           subsequent_indent=indent)
            message = f"\n{self.get_invalid_response_object(key_to_object, method, status_code)}"
            string_to_print += prefix + wrapper.fill(message) + "\n"
        return string_to_print + "\n\n" if string_to_print != "" else ""

    # ************** CREATE OBJECTS **************** #

    def __set_objects(self):
        self.objects = {}
        for key, schema_value in self.__schemas.items():
            self.objects.update({key: {}})
            for method in schema_value.keys():
                self.objects[key].update({method: {}})
                if "requestBody" in schema_value[method].keys():
                    self.__set_request_body(key, method)
                if "responses" in schema_value[method].keys() and self.__response_gen:
                    self.__set_responses(key, method, schema_value[method])

    def __set_responses(self, endpoint, method, schema_value):
        self.objects[endpoint][method].update({"responses": {}})
        for res_num, res_val in schema_value["responses"].items():
            self.__set_response_body(endpoint, method, res_num)

    def __set_response_body(self, endpoint, method, res_num):
        self.objects[endpoint][method]["responses"].update(
            {res_num: self.__generate_response_object(endpoint, method, str(res_num))})

    def __set_request_body(self, endpoint, method):
        self.objects[endpoint][method].update({"requestBody": self.__generate_request_object(endpoint, method)})

    def __generate_request_object(self, endpoint, method):
        cache_pack = {"title": "request", "endpoint": endpoint, "method": method}
        schema_value = self.__schemas[endpoint][method]["requestBody"]
        return ObjectsGenerator(schema_value, self.__config, self.__generate_invalid, self.__cache_dir, cache_pack)

    def __generate_response_object(self, endpoint, method, res_num):
        cache_pack = {"title": "response", "endpoint": endpoint, "method": method, "res_num": str(res_num)}
        schema_value = self.__schemas[endpoint][method]["responses"][str(res_num)]
        return ObjectsGenerator(schema_value, self.__config, self.__generate_invalid, self.__cache_dir, cache_pack)

    # ************** EDIT OBJECTS **************** #

    @staticmethod
    def __fetch_invalid_object_ls(invalid_ls, with_info):
        if with_info:
            return invalid_ls
        return [obj.get("data") for obj in invalid_ls]

    @staticmethod
    def __fetch_data(obj, change={}, add={}, remove={}, required_object=False, min_val_object=False):
        if obj:
            if min_val_object:
                object_to_scan = obj.min_val_object
            elif required_object:
                object_to_scan = obj.required_object
            else:
                object_to_scan = obj.full_object
            return OpenApiDataGenerator.__edit_dict(deepcopy(object_to_scan), change, add, remove)

    @staticmethod
    def __remove_packs(fields_to_remove, ret):
        if isinstance(ret, dict):
            demo = ret.copy()
            if fields_to_remove:
                for key, value in demo.items():
                    if key in fields_to_remove:
                        del ret[key]
                    if isinstance(value, dict):
                        OpenApiDataGenerator.__remove_packs(fields_to_remove, ret[key])

    @staticmethod
    def __edit_dict(object_to_scan, change, add, remove):
        key_errors = []
        if isinstance(object_to_scan, dict):
            return OpenApiDataGenerator.__edit_single_dict(add, change, remove, key_errors, object_to_scan)
        if isinstance(object_to_scan, list):
            for i in range(len(object_to_scan)):
                object_to_scan[i] = OpenApiDataGenerator.__edit_single_dict(add, change, remove, key_errors,
                                                                            object_to_scan[i])
            return object_to_scan

    @staticmethod
    def __edit_single_dict(fields_to_add, fields_to_change, fields_to_remove, key_errors, object_to_scan):
        if isinstance(fields_to_change, dict):
            for key, value in fields_to_change.items():
                change = ObjectsGenerator.set_single_value(object_to_scan, key, value)
                if change is False:
                    key_errors.append(key)
        OpenApiDataGenerator.__remove_packs(fields_to_remove, object_to_scan)
        if fields_to_add:
            object_to_scan.update(fields_to_add)
        return object_to_scan

    @staticmethod
    def __set_values_in_settings(object_to_set_in, **kwargs):
        for key, value in kwargs.items():
            if value:
                object_to_set_in[key] = value
