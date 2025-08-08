# ordl_framework/core/odrl_enforcer.py
import operator
from .metrics_registry import metrics_registry
from .actions_registry import actions_registry

OPS = {
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
    "==": operator.eq,
    "!=": operator.ne,
}

class ODRLEnforcer:
    def __init__(self, objects: dict, policies: list):
        """
        objects: dict mapping object_id -> model instance (ej. 'storage_vehiculo_1' -> Storage(...))
        policies: list of policy dicts (como en example.ordl.json)
        """
        self.objects = objects
        self.policies = policies

    def _resolve_metric(self, target_id, metric_name):
        # 1) intento provider registrado por clave exacta
        key_exact = f"{target_id}.{metric_name}"
        provider = metrics_registry.get_provider(key_exact)
        if provider:
            return provider()

        # 2) intento provider por tipo genérico (ej. 'storage.used_percent')
        # si el objeto tiene tipo o convención, se puede ampliar aquí.
        provider = metrics_registry.get_provider(metric_name)
        if provider:
            return provider(target_id) if provider.__code__.co_argcount else provider()

        # 3) fallback: si el objeto tiene un método del metric_name, lo usamos (ej. used_percent)
        obj = self.objects.get(target_id)
        if obj and hasattr(obj, metric_name):
            meth = getattr(obj, metric_name)
            return meth() if callable(meth) else meth

        raise RuntimeError(f"No metric provider for '{key_exact}' or '{metric_name}' and object '{target_id}' lacks attribute.")

    def evaluate_policies(self):
        results = []
        for p in self.policies:
            target = p["target"]
            cond = p["condition"]
            metric_name = cond["metric"]
            op = cond["operator"]
            threshold = cond["value"]

            try:
                metric_value = self._resolve_metric(target, metric_name)
            except Exception as e:
                results.append((p["id"], False, f"error resolving metric: {e}"))
                continue

            ok = OPS[op](metric_value, threshold)

            if ok:
                action_spec = p["action"]
                if action_spec["type"] == "call":
                    func_name = action_spec["function"]
                    # args from policy + add context if wanted
                    args = action_spec.get("args", [])
                    # permitimos pasar el id del target a la acción
                    actions_registry.execute(func_name, target, *args)
                results.append((p["id"], True, metric_value))
            else:
                results.append((p["id"], False, metric_value))
        return results
