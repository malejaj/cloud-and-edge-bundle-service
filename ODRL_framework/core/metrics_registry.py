# ordl_framework/core/metrics_registry.py
from typing import Callable

class MetricsRegistry:
    def __init__(self):
        self._providers = {}  # key -> callable (no-arg or (target)->value)

    def register(self, key: str, func: Callable):
        """Register a metric provider under a key (e.g. 'storage_vehiculo_1.used_percent' or 'storage.used_percent')."""
        self._providers[key] = func

    def get_provider(self, key: str):
        return self._providers.get(key)

# instancia global (opcional)
metrics_registry = MetricsRegistry()
