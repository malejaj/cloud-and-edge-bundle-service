# core/registry.py (estructura típica)
class BuilderRegistry:
    def __init__(self):
        self._registry = {}

    def register(self, key):
        def decorator(builder_func):
            self._registry[key] = builder_func
            return builder_func
        return decorator
    def add(self, key, builder_func):
        self._registry[key] = builder_func

    def build(self, key, data):
        if key not in self._registry:
            raise ValueError(f"No builder registered for '{key}'")
        return self._registry[key](data)

    def keys(self):
        return self._registry.keys()

# instancia global
builder_registry = BuilderRegistry()
