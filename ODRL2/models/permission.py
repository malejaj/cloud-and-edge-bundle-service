from registry import register_class

@register_class
class Permission:
    def __init__(self, action, target, constraints=None):
        self.action = action
        self.target = target
        self.constraints = constraints or []

    def __repr__(self):
        return f"<Permission action={self.action} target={self.target} constraints={self.constraints}>"

    def check_constraints(self, context):
        # Todas las constraints deben cumplirse para permitir la acción
        return all(c.is_satisfied(context) for c in self.constraints)
