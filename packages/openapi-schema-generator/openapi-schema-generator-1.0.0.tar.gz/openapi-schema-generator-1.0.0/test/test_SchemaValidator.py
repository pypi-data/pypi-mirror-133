from openapi_schema_generator.OpenApiSchemaValidator import OpenApiSchemaValidator
from copy import deepcopy

request_endpoint = "/pet"
response_endpoint = "/store/order"

full_request_data = {
    "id": 10,
    "name": "doggie",
    "category": {
        "id": 1,
        "name": "Dogs"
    },
    "photoUrls": [
        "string"
    ],
    "tags": [
        {
            "id": 0,
            "name": "string"
        }
    ],
    "status": "available"
}

full_response_data = {
    "id": 10,
    "petId": 198772,
    "quantity": 7,
    "shipDate": "2021-12-30T10:21:57.309Z",
    "status": "approved",
    "complete": True
}

validator = OpenApiSchemaValidator(f"test/Examples/src/petstore.json")


# ***************** REQUEST ******************** #


def test_request_valid():
    relevant_data = full_request_data
    assert validator.validate_request_schema(request_endpoint, relevant_data) is True


def test_request_valid_missing_high_level_optional():
    relevant_data = deepcopy(full_request_data)
    relevant_data.pop("tags")
    assert validator.validate_request_schema(request_endpoint, relevant_data) is True


def test_request_not_valid_high_level_field_not_exist():
    relevant_data = deepcopy(full_request_data)
    relevant_data.update({"not_exist": 3})
    assert validator.validate_request_schema(request_endpoint, relevant_data) is True


def test_request_not_valid_low_level_field_not_exist():
    relevant_data = deepcopy(full_request_data)
    relevant_data['category'].update({"not_exist": 3})
    assert validator.validate_request_schema(request_endpoint, relevant_data) is True


def test_request_not_valid_missing_require_high_level():
    relevant_data = deepcopy(full_request_data)
    relevant_data.pop("name")
    assert validator.validate_request_schema(request_endpoint, relevant_data) is False


def test_request_not_valid_give_string_not_from_enum():
    relevant_data = deepcopy(full_request_data)
    relevant_data["status"] = "not exist"
    assert validator.validate_request_schema(request_endpoint, relevant_data) is False


# ***************** RESPONSE ******************** #


def test_response_valid():
    relevant_data = deepcopy(full_response_data)
    assert validator.validate_response_schema(response_endpoint, relevant_data, method='post') is True


def test_response_valid_missing_high_level_optional():
    relevant_data = deepcopy(full_response_data)
    relevant_data.pop("id")
    assert validator.validate_response_schema(response_endpoint, relevant_data, method='post') is True


def test_response_not_valid_high_level_field_not_exist():
    relevant_data = deepcopy(full_response_data)
    relevant_data.update({"not_exist": 3})
    assert validator.validate_response_schema(response_endpoint, relevant_data, method='post') is True


def test_response_not_valid_wrong_type():
    relevant_data = deepcopy(full_response_data)
    relevant_data['id'] = "string"
    assert validator.validate_response_schema(response_endpoint, relevant_data, method='post') is False


def test_response_not_valid_give_string_not_from_enum():
    relevant_data = deepcopy(full_response_data)
    relevant_data['status'] = 'not_exist'
    assert validator.validate_response_schema(response_endpoint, relevant_data, method='post') is False
