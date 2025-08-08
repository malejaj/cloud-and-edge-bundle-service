# ordl_framework/core/builder.py
import json
from pathlib import Path
from .registry import builder_registry

def build_objects_from_ordl(file_path):
    base_path = Path(__file__).resolve().parent.parent  # sube de core/ a ODRL_framework/
    file_path = (base_path / file_path).resolve()
    with open(file_path, "r") as f:
        raw_data = json.load(f)

    objects = {}
    for obj_type, obj_data in raw_data.items():
        objects[obj_type] = builder_registry.build(obj_type, obj_data)
    return objects
