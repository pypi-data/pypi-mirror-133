

- Description:
	```
	This submodule supply single object - OpenApiDataGenerator
	Main argument is path of to 'open api' specification and gives some utils -
		OpenApiDataGenerator - 
			1. Generate objects by thier schemas with default value - for any endpoint on server. Request body and response body.
			2. Between two ends - require object and full object - thier are many combinations of valid objects. 
			You can get those by all possible options at list, or random object any time.
	```

- Prerequisite:

    - Install requirements:
        ```
        pip install -r requirements.txt
        ```
  
- Usage:
    - Testing tools:
        ```
        python -m openapi_data_generator --path=<openapi_root_path>
        Flags:
            --generate_responses = tool generates responses objects
            --generate_invalid = tool generates invalid object
            --use_cache = generate files at .api_cache_dir folder
            --restart_cache = regenerate cache folder

        ```
    
    - Imports:
        ```
        from openapi_data_generator import OpenApiDataGenerator
        ```
		
    - Create a reference to your configuration:
        ```
        my_generator = OpenApiDataGenerator(path=<path for main file>, generate_responses=False <True give responses object also>, generate_invalid=False <True give invalid object also>)
        ```
    
	- OpenApiDataGenerator:
		```
		some_endpoint = <some_endpoint> # generator relate to valid endpoint with '/' at start and without '/' at end -  Example "/valid/endpoint"
		method = 'post'
		some_endpoint_data = my_generator.get_<require/full/random/invalid/min_val>_request_object(endpoint=some_endpoint, method=method, change={}, add={}, remove={})
		some_endpoint_data = my_generator.get_<require/full/random/invalid/min_val>_response_object(endpoint=some_endpoint, response_num=200,method=method, change={}, add={}, remove={})
	
	    # Advance - in case you want to change the default optional criteria , send key values
	    
	    In order to change settings at any created instance:
	        OpenApiDataGenerator.set_general_behavior(key=value)
	    In order to change settings for specific instance:
	        my_generator.set_instance_behavior(key=value)
	        
        Possible keys to set --> [array_min_items, array_max_items, default_probability, nullable_probability, max_str_length, min_int, max_int, min_float, max_float]



		NOTE!
			Any object is generated with default values. Therefore thier are 2 options:
				1. At any request you can mention changes you want to do - change, add, remove - dictionaries of 'key' : 'request_new_value' (remove is set of keys).
				2. Another similar method is 'set_and_change_default_<request/response>_values' - with same argument - you can change the default value and all objects 
					you will request from now on own this default value.

		```

- Support:
	- Open api version:
		```

		Support at 'open api' 3.0.0 version. 
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
