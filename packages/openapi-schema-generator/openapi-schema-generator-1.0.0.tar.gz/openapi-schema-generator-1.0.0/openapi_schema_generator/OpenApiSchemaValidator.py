from .OpenApiSchemaGenerator import OpenApiSchemaGenerator
from jsonschema import exceptions
from openapi_schema_validator import OAS30Validator


class OpenApiSchemaValidator(object):
    def __init__(self, path):
        generator = OpenApiSchemaGenerator(path)
        self._schemas = generator.build_mapped_schema()

    def validate_request_schema(self, endpoint, data, method='post'):
        relevant_schema = self.get_request_schema_from_spec(endpoint, method)
        return self.__validation(relevant_schema, data)

    def validate_response_schema(self, endpoint, data, method='get', res_number=200):
        relevant_schema = self.get_response_schema_from_spec(endpoint, method, res_number)
        return self.__validation(relevant_schema, data)

    def __validation(self, relevant_schema, data):
        if relevant_schema and not self.is_json_valid(data, relevant_schema):
            return False
        return True

    def validate_request_schema_with_reason(self, endpoint, data, method='post'):
        relevant_schema = self.get_request_schema_from_spec(endpoint, method)
        return self.__validation_with_reason(relevant_schema, data)

    def validate_response_schema_with_reason(self, endpoint, data, method='get', res_number=200):
        relevant_schema = self.get_response_schema_from_spec(endpoint, method, res_number)
        return self.__validation_with_reason(relevant_schema, data)

    def __validation_with_reason(self, relevant_schema, data):
        if relevant_schema:
            result = self.is_json_valid_with_reason(data, relevant_schema)
            return result
        return False, "Object not exist!"

    def get_request_schema_from_spec(self, endpoint, method):
        method = method.lower()
        if method in self._schemas[endpoint] and 'requestBody' in self._schemas[endpoint][method]:
            base_schema = self._schemas[endpoint][method]["requestBody"]
            return base_schema

    def get_response_schema_from_spec(self, endpoint, method, res_number):
        method = method.lower()
        if method in self._schemas[endpoint] and \
                'responses' in self._schemas[endpoint][method] and \
                str(res_number) in self._schemas[endpoint][method]['responses']:
            base_schema = self._schemas[endpoint][method]['responses'][str(res_number)]
            return base_schema

    @staticmethod
    def is_json_valid(data, require_schema):
        try:
            schema_object = OAS30Validator(require_schema)
            schema_object.validate(data)
        except exceptions.ValidationError:
            return False
        return True

    @staticmethod
    def is_json_valid_with_reason(data, require_schema):
        try:
            schema_object = OAS30Validator(require_schema)
            schema_object.validate(data)
        except exceptions.ValidationError as e:
            return False, e
        return True, "Object is Valid!"
