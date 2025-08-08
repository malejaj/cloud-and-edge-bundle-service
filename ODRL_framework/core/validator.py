# ordl_framework/core/validator.py
import json
from jsonschema import validate
from pathlib import Path

def validate_odrl(file_path, schema_path):
    base_path = Path(__file__).resolve().parent.parent  # sube de core/ a ODRL_framework/
    file_path = (base_path / file_path).resolve()
    schema_path = (base_path / schema_path).resolve()
    with open(file_path, "r") as f:
        raw_data = json.load(f)
    with open(schema_path, "r") as s:
        schema = json.load(s)

    validate(instance=raw_data, schema=schema)
    return raw_data
