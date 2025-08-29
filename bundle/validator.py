import json
from jsonschema import validate, ValidationError

def validate_ordl(ordl_path, schema_path):
    with open(ordl_path, "r") as f:
        raw_data = json.load(f)
    with open(schema_path, "r") as f:
        schema = json.load(f)

    try:
        validate(instance=raw_data, schema=schema)
        print("ODRL is valid.")
    except ValidationError as e:
        raise ValueError(f"ODRL Validation Error: {e.message}")
    return raw_data
