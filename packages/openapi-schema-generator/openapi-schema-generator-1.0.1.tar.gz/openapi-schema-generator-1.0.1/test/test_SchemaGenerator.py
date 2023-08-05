from openapi_schema_generator import OpenApiSchemaGenerator
from compare_objects import compare_objects
import json
import yaml

# **************** Globals ***************** #

base_path = "test/Examples"


def get_expected_and_gen(file_name, file_type='json'):
    src_path = f"{base_path}/src/{file_name}.{file_type}"
    result_path = f"{base_path}/results/{file_name}_result.{file_type}"
    gen = OpenApiSchemaGenerator(src_path)
    with open(result_path, 'r') as f:
        if 'yaml' in result_path:
            return yaml.load(f, yaml.FullLoader), gen.deploy_schema()
        else:
            return json.load(f), gen.deploy_schema()


# ******************* MULTI HIERARCHICAL ******************* #


# def test_json_schema_with_multi_hierarchical():
#     data, generated_schemas = get_expected_and_gen("multi_hierarchical", "multi_hierarchical/multi_hierarchical.json")
#     assert compare_objects(data, generated_schemas)


# ******************* HIERARCHICAL ******************* #

# def test_json_schema_with_hierarchical():
#     data, generated_schemas = get_expected_and_gen("hierarchical", "json")
#     assert compare_objects(data, generated_schemas)
#
#
# def test_yaml_schema_with_hierarchical():
#     data, generated_schemas = get_expected_and_gen("hierarchical", "yaml")
#     assert compare_objects(data, generated_schemas)


# ******************* REF FOR COMPONENTS ******************* #

def test_json_schema_with_ref_for_comp():
    data, generated_schemas = get_expected_and_gen("petstore", "json")
    assert compare_objects(data, generated_schemas)


def test_yaml_schema_with_ref_for_comp():
    data, generated_schemas = get_expected_and_gen("petstore", "yaml")
    assert compare_objects(data, generated_schemas)


# ******************* ALL IN ONE ******************* #

def test_json_schema_with_all_in_one():
    data, generated_schemas = get_expected_and_gen("jobs", "json")
    assert compare_objects(data, generated_schemas)


def test_yaml_schema_with_all_in_one():
    data, generated_schemas = get_expected_and_gen("jobs", "yaml")
    assert compare_objects(data, generated_schemas)



