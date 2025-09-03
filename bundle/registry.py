CLASS_REGISTRY = {}

def register_class(cls):
    """Decorator to register classes by name."""
    CLASS_REGISTRY[cls.__name__] = cls
    return cls


def build_object(obj_data):
    """Build an object dynamically from a dict (recursive)."""
    if not isinstance(obj_data, dict):
        return obj_data

    obj_type = obj_data.get("type")
    print(f"Building object of type: {obj_type}")

    if obj_type:  
        cls = CLASS_REGISTRY.get(obj_type)
        print(f"Found class: {cls}")
        if not cls:
            raise ValueError(f"Unknown class type: {obj_type}")

        kwargs = {}
        for k, v in obj_data.items():
            if k == "type":
                continue

            # Recursion
            if isinstance(v, dict):
                kwargs[k] = build_object(v)
            elif isinstance(v, list):
                kwargs[k] = [build_object(i) if isinstance(i, dict) else i for i in v]
            else:
                kwargs[k] = v
        if "constraints" in kwargs and kwargs["constraints"] is None:
            kwargs["constraints"] = []
       
        return cls(**kwargs)

    # If there's no "type", we recursively build sub-elements
    return {k: build_object(v) for k, v in obj_data.items()}
