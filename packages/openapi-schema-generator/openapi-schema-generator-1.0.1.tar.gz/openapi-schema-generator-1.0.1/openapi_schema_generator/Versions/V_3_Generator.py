from copy import deepcopy
from openapi_schema_generator.FilePathTracker import FilePathTracker
from .AbsGenerator import AbstractGenerator


class V3Generator(AbstractGenerator):
    def __init__(self):
        AbstractGenerator.__init__(self)
        self.__file_tracker = self.__root_data = None

    # ********************************** MAIN FUNCTION THAT HANDLE ALL OPERATION      ****************************** #

    def __set_path_to_system(self, path):
        self.__file_tracker = FilePathTracker(path)
        self.__root_data = self.__file_tracker.get_root_data()

    def deploy_schema(self, path: str) -> dict:
        self.__set_path_to_system(path)
        self.__handle_component_schema()
        for section_key in self._sections_keys:
            section = self.__root_data.get(section_key, {})
            for endpoint in section:
                self.__iterate_on_endpoint_methods(endpoint, section)
        return self.__root_data

    def build_mapped_schema(self, path: str, content_type='application/json') -> dict:
        data = {}
        self.__set_path_to_system(path)
        for section_key in self._sections_keys:
            section = self.__root_data.get(section_key, {})
            for endpoint, value in section.items():
                data.update({endpoint: {}})
                self.__iterate_on_endpoint_methods_with_map_data(endpoint, section, data, content_type)
        return data

    # ********************************** FILL ALL ENDPOINTS WITH REFERENCES OR BASIC SCHEMA************************** #

    # State D - deploy & map data
    def __handle_schema(self, schema):
        if "$ref" in schema:
            reference = schema["$ref"]
            return self.start_generate_from_reference(reference, is_root=True)
        else:
            return self.start_generate_by_properties(schema, schema)

    # State C - deploy & map data
    def __handle_content(self, content):
        if 'schema' in content:
            result = self.__handle_schema(content['schema'])
            content['schema'] = result

    # State B - deploy & map data
    def __fill_in_request_body_schema(self, root_schema, content_type):
        ret_data = None
        if "content" in root_schema:
            for content_key in root_schema['content']:
                self.__handle_content(root_schema['content'][content_key])
                if content_key == content_type:
                    ret_data = root_schema['content'][content_key]['schema']
        if 'schema' in root_schema:
            self.__handle_content(root_schema)
        return ret_data

    # State B - deploy
    def __fill_in_responses_body_schema(self, root_schema, content_type):
        for res_num in root_schema:
            self.__fill_in_request_body_schema(root_schema[res_num], content_type)

    # State B - map data
    def __fill_in_responses_body_schema_with_map_data(self, root_schema, data, content_type):
        for res_num in root_schema:
            result = self.__fill_in_request_body_schema(root_schema[res_num], content_type)
            data['responses'].update({res_num: result})

    # State A - deploy
    def __iterate_on_endpoint_methods(self, endpoint, section, content_type=None):
        for method in self._methods:
            method_section = section[endpoint].get(method, {})
            if 'requestBody' in method_section:
                self.__fill_in_request_body_schema(section[endpoint][method]['requestBody'], content_type)
            if 'responses' in method_section:
                self.__fill_in_responses_body_schema(section[endpoint][method]['responses'], content_type)

        self.__fill_in_parameters(endpoint, section)

    # State A - map data
    def __iterate_on_endpoint_methods_with_map_data(self, endpoint, section, data, content_type):
        for method in self._methods:
            if method in section[endpoint]:
                data[endpoint].update({method: {}})
                if 'requestBody' in section[endpoint][method]:
                    result = self.__fill_in_request_body_schema(section[endpoint][method]['requestBody'], content_type)
                    data[endpoint][method].update({'requestBody': result})
                if 'responses' in section[endpoint][method]:
                    data[endpoint][method].update({'responses': {}})
                    self.__fill_in_responses_body_schema_with_map_data(section[endpoint][method]['responses'],
                                                                       data[endpoint][method], content_type)

    # ~~~~~ State A extra operations ~~~~~~~ #

    # State B - (deploy parameters)
    def __handle_parameters_schemas(self, content):
        if 'schemas' in content:
            for i in range(len(content['schemas'])):
                if 'schema' in content['schemas'][i]:
                    content['schemas'][i]['schema'] = self.__handle_schema(content['schemas'][i]['schema'])

    # State A - (deploy parameters)
    def __fill_in_parameters(self, endpoint, section):
        root_schema = section[endpoint].get('parameters', {})
        if "content" in root_schema:
            for content_key in root_schema['content']:
                self.__handle_parameters_schemas(root_schema['content'][content_key])
        self.__handle_parameters_schemas(root_schema)

    # State A - (deploy component schemas)
    def __handle_component_schema(self):
        if 'components' in self.__root_data and 'schemas' in self.__root_data['components']:
            for key in self.__root_data['components']['schemas']:
                result = self.__handle_schema(self.__root_data['components']['schemas'][key])
                self.__root_data['components']['schemas'].update({key: result})

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    # ********************************** REPLACE ALL REFERENCES WITH REAL SCHEMA ****************************** #

    @staticmethod
    def get_from_schema_ref_file_and_data(string):
        # return from 'file # nested_key' --> <file>, <nested_key>
        ls = string.split("#")
        if len(ls) == 1:
            ls.append("")
        else:
            ls[1] = ls[1][1:]
        return ls

    def get_reference_from_components(self, schema_ref):
        # return value from components/schemas
        root_data = self.__root_data
        ref_key = schema_ref.split("/")[-1]
        # options:
        #       1. relevant schema
        #       2. ref to file that contain multiple keys 'file # nested_key' \ file that represent the nested schema
        return root_data['components']['schemas'][ref_key].get('$ref', root_data['components']['schemas'][ref_key])

    def __extract_data_from_sub_file(self, source_file, specific_data):
        # return data leaf data by splits key
        # data = self.fetch_node_data(source_file)
        data = self.__file_tracker.fetch_node_data(source_file)
        splits_key = specific_data.split("/")
        for key in splits_key[:-1]:
            data = data[key]
        return data, source_file, splits_key[-1]

    def get_file_data_and_key_to_req_data(self, schema_ref, source_file):
        if "json" in schema_ref or "yml" in schema_ref or "yaml" in schema_ref:
            # spilt reference from 'file # requested_key' to file and req_key
            source_file, req_key = self.get_from_schema_ref_file_and_data(schema_ref)
            # if file is the key fetch the data , file , and last key in hierarchy
            if req_key != "":
                return self.__extract_data_from_sub_file(source_file, req_key)
            # fetch data, source_file, and key
            return self.__file_tracker.fetch_node_data(source_file), source_file, req_key
        elif isinstance(schema_ref, str):
            # if its valid reference - data, source_file, req_key
            return self.__file_tracker.fetch_node_data(source_file), source_file, schema_ref[2:]

        # if reference is not valid - return values as is
        return schema_ref, source_file, ""

    # ****************************** RECURSIVE ITERATION ON SCHEMAS FILES AND REFERENCES **************************** #

    # State D -- move to  A, B
    def trace_forward_data(self, source_file, root_schema, specific_data, parent, parent_key):
        source_property = parent[parent_key]

        if "properties" in source_property:
            # recursive call for nested object
            self.run_all_over_schema_keys(source_property["properties"], root_schema, specific_data, source_file)
        if "$ref" in source_property:
            # get the extra definition data
            external_schema_to_set = self.start_generate_from_reference(parent[parent_key]['$ref'], source_file)
            parent[parent_key] = external_schema_to_set[list(external_schema_to_set.keys())[0]]

    # State C -- move to D
    def scan_properties_internals(self, schema_to_fill, specific_data, source_file, parent, parent_key):
        source_property = parent[parent_key]
        if "oneOf" in source_property or 'anyOf' in source_property:
            rel_key = 'oneOf' if "oneOf" in source_property else 'anyOf'
            for index in range(len(source_property[rel_key])):
                self.trace_forward_data(source_file, schema_to_fill, specific_data, source_property[rel_key], index)
        else:
            self.trace_forward_data(source_file, schema_to_fill, specific_data, parent, parent_key)

    # State B -- move to C
    def run_all_over_schema_keys(self, properties, schema_to_fill, specific_data, source_file):
        for key in properties:
            # dive in list
            if "items" in properties[key]:
                self.scan_properties_internals(schema_to_fill, specific_data, source_file, properties[key], "items")

            # dive in dict
            self.scan_properties_internals(schema_to_fill, specific_data, source_file, properties, key)

    # State A -- move to B, C
    def start_generate_by_properties(self, schema_body, schema_to_fill_in, source_file=None, specific_data=None):
        # in case of start with dict
        if "properties" in schema_body:
            self.run_all_over_schema_keys(schema_body["properties"], schema_to_fill_in, specific_data, source_file)

        # in case of start with list
        elif "items" in schema_body:
            self.scan_properties_internals(schema_to_fill_in, specific_data, source_file, schema_body, "items")
        # extract schema from root key
        schema_root_key = list(schema_to_fill_in.keys())
        if len(schema_root_key) > 0 and "root_data" in schema_root_key[0]:
            return schema_to_fill_in[schema_root_key[0]]
        return schema_to_fill_in

    # State A
    def start_generate_from_reference(self, schema_ref, source_file=None, is_root=False):
        keep_origin = deepcopy(schema_ref)
        if "components/schemas" in schema_ref:
            schema_ref = self.get_reference_from_components(schema_ref)

        file_data, source_file, req_key = self.get_file_data_and_key_to_req_data(schema_ref, source_file)
        # if req key is empty - sub schema represented by isolated file - therefore key is file name
        if req_key == "":
            req_key = self.__use_filename_as_key(keep_origin, source_file)
            req_key = f"{req_key}_root_data" if is_root else req_key
            schema = {req_key: file_data}
        # if req key is empty - sub schema represented by isolated file - therefore key is file name
        else:
            # in case file data contain several keys - look for requested_key
            schema_value = file_data[req_key]
            req_key = f"{req_key}_root_data" if is_root else req_key
            schema = {req_key: schema_value}
            file_data = schema_value
        return self.start_generate_by_properties(file_data, schema, source_file, req_key)

    @staticmethod
    def __use_filename_as_key(keep_origin, source_file):
        if source_file:
            path = source_file.split("/")
            # remove '.<file_type>' from file name (yml - 4 letters; yaml & json - letters)
            key = path[len(path) - 1][:-4] if "yml" in path[len(path) - 1] else path[len(path) - 1][:-5]
        else:
            key = keep_origin.split("/")[-1]
        return key
