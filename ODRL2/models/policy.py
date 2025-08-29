from registry import register_class

@register_class
class Policy:
    def __init__(self, id, permissions=None, duties=None):
        self.id = id
        self.permissions = permissions or []
        self.duties = duties or []

    def __repr__(self):
        return f"<Policy {self.id} - {len(self.permissions)} perms, {len(self.duties)} duties>"

    def is_action_allowed(self, action, target, context):
        # Busca permiso que coincida en acción y objetivo
        for perm in self.permissions:
            if perm.action == action and perm.target == target:
                return perm.check_constraints(context)
        return False
