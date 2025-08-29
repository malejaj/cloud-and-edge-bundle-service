# policy_engine.py
from registry import CLASS_REGISTRY
from bundle.Model import Policy


class PolicyRunner:
    def __init__(self, policy: Policy):
        self.policy = policy

    def execute(self):
        print("🚀 Executing Policy...")

        # Ejecutar permisos
        if self.policy.rules:
            print("🔹 Handling Rules")
            for rule in self.policy.rules:
                if rule.type == "permission":
                    self._handle_permission(rule)
                elif rule.type == "duty":
                    self._handle_duty(rule)

        # Ejecutar deberes
        if self.policy.duties:
            print("🔹 Handling Duties")
            for duty in self.policy.duties:
                self._handle_duty(duty)

        # Puedes añadir prohibitions si las usas
        if self.policy.prohibitions:
            print("🔹 Handling Prohibitions (not implemented yet)")

    def _handle_permission(self, permission):
        action = permission.action
        target = permission.target

        print(f"   → Permission: action={action}, target={target}")

        # Buscar si el target está en el registro de clases
        if target in CLASS_REGISTRY:
            obj_class = CLASS_REGISTRY[target]
            obj_instance = obj_class()

            if hasattr(obj_instance, action):
                method = getattr(obj_instance, action)
                print(f"      ✅ Executing {target}.{action}()")
                method()
            else:
                print(f"      ⚠️ Target '{target}' does not support action '{action}'")
        else:
            print(f"      ⚠️ Target '{target}' not found in registry")

    def _handle_duty(self, duty):
        action = duty.action
        target = duty.target

        print(f"   → Duty: action={action}, target={target}")

        # Igual que en permission
        if target in CLASS_REGISTRY:
            obj_class = CLASS_REGISTRY[target]
            obj_instance = obj_class()

            if hasattr(obj_instance, action):
                method = getattr(obj_instance, action)
                print(f"      ✅ Executing {target}.{action}() as duty")
                method()
            else:
                print(f"      ⚠️ Duty target '{target}' does not support action '{action}'")
        else:
            print(f"      ⚠️ Duty target '{target}' not found in registry")
