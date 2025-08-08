# ordl_framework/core/actions_registry.py
from typing import Callable

class ActionsRegistry:
    def __init__(self):
        self._actions = {}

    def register(self, name: str, func: Callable):
        self._actions[name] = func

    def get(self, name: str):
        return self._actions.get(name)

    def execute(self, name: str, *args, **kwargs):
        f = self.get(name)
        if not f:
            raise ValueError(f"Action '{name}' not registered")
        return f(*args, **kwargs)

actions_registry = ActionsRegistry()
