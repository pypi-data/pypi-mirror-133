from ast import literal_eval
from .FilePathTracker import FilePathTracker
from openapi_schema_generator.Versions.V_2_Generator import V2Generator
from openapi_schema_generator.Versions.V_3_Generator import V3Generator
from openapi_schema_generator.Versions.AbsGenerator import AbstractGenerator


class OpenApiSchemaGenerator(object):
    def __init__(self, path):
        self.path = path
        self.__generator = self.get_generator()

    def deploy_schema(self):
        return self.__generator.deploy_schema(self.path)

    def build_mapped_schema(self):
        return self.__generator.build_mapped_schema(self.path)

    def set_path(self, path):
        self.__init__(path)

    def get_generator(self) -> AbstractGenerator:
        root_data = FilePathTracker(self.path).get_root_data()
        open_api_main_version = OpenApiSchemaGenerator.__get_open_api_version(root_data)
        if open_api_main_version == 3:
            return V3Generator()
        if open_api_main_version == 2:
            return V2Generator()
        raise AbstractGenerator.OpenApiVersionError(
            "This module supports at open api version 3.0.0. Your openapi file version is not"
            " support. Please convert your file to correct version. Optional converters at "
            "http://editor.swagger.io, or at http://mermade.org.uk/openapi-converter")

    @staticmethod
    def __get_open_api_version(root_data):
        if "openapi" in root_data:
            key_for_version = root_data["openapi"]
        elif "swagger" in root_data:
            key_for_version = root_data["swagger"]
        else:
            raise AbstractGenerator.OpenApiVersionError("Module cannot recognize OpenApi version from the given file")

        return literal_eval(key_for_version.split(".")[0])