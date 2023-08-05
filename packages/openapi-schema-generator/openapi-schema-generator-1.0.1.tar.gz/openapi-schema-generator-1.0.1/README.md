
- Description:
	```
	This submodule supply two objects - OpenApiSchemaGenerator and OpenApiSchemaValidator.
	Each one gets path of to 'open api' specification and gives some utils -
		OpenApiSchemaGenerator - 
			1. Generate full schema, 'open' all references to one file hierarchy.
			2. Generate all schema from any version to one specific ,dedicated to schema, object.
			
		OpenApiSchemaValidator - 
			1. Hold all server endpoints schemas - and gives the utility to validate any object with its schema automatically.
			2. In case its usefull - get swagger schema dynamically by endpoint and method.
	```

- Prerequisite:
    - Install requirements:
        ```
        pip install -r requirements.txt
        ```
  
- Usage:
    - Testing tools:
        ```
        python -m openapi_schema_generator --path=<openapi_root_path> --output=<(default)result.json>
        
        ```
    
    - Imports:
        ```
        from openapi_schema_generator import OpenApiSchemaGenerator
		from openapi_schema_generator import OpenApiSchemaValidator
        ```
		
    - Create a reference to your configuration:
        ```
        my_generator = OpenApiSchemaGenerator(path=<path for main file>)
		my_validator = OpenApiSchemaValidator(path=<path for main file>)
        ```
    
	- OpenApiSchemaGenerator:
		```
		result = my_generator.deploy_schema() # give union schema file for specified path
        result = my_generator.build_mapped_schema() # create unioned schema file(for all versions)
        
        my_generator.set_path(path=<path for main file>) # new path to handle

		```
		
    - OpenApiSchemaValidator:
		```
		some_endpoint = <some_endpoint>
		method = 'get'
		data = <some data>
		validate_request_schema(endpoint=some_endpoint, data=data, method=method)
		validate_response_schema(endpoint=some_endpoint, data=data, method=method, res_number=200)
		```
	- Note:
		```
		As a default behavior - default method for request method is 'post', and for response method is 'get'.
		You can use it for save text most of the times instead specify methods.
		```

- Support:
	- Open Api version:
		```

		Support at 'open api' 3.0.0 version.
		Support at 'open api' 2 - not implemented yet.
		For earlier version you could convert your spec files by convertors as http://editor.swagger.io, or at http://mermade.org.uk/openapi-converter.
		```

	- Files:
		```
		Support both types of swagger files - Yaml and Json.
		```

	- Files layout:
		```

		Support at 3 kinds of layouts
			1. All schemas at one single file.
			2. Any object at main file refer to specific general field called 'components'-'schemas'.
			This field relate any schema to other general file with specification to its relevat field.
			3. Any object at main file refer to its specific file in folder hierarchy. The Root is main file's directory.
		```

