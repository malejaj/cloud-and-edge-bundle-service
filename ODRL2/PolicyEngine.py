from bundle.Model import Policy, Permission, Prohibition, Duty, Event, Capability


class PolicyEngine:
    """Middleware que gestiona eventos y aplica políticas ODRL."""
    def __init__(self):
        self.capabilities: dict[str, Capability] = {}
        self.policies: list[Policy] = []
        self.events: dict[str, Event] = {}

    def register_capability(self, capability: Capability):
        self.capabilities[capability.asset.uid] = capability

    def register_policy(self, policy: Policy):
        self.policies.append(policy)

    def handle_event(self, event: Event):
        """Recibe un evento de una capacidad y evalúa las políticas."""
        self.events[event.source_uid] = event
        print(f"[ENGINE] Evento recibido: {event}")

        for policy in self.policies:
            for rule in policy.rules:
                # --- Duty ---
                if isinstance(rule, Duty) and rule.target.uid == event.source_uid:
                    print(f"[ENGINE] Duty cumplido: {rule.uid} por {event.source_uid}")

                # --- Permission ---
                if isinstance(rule, Permission):
                    if rule.target.uid in self.capabilities:
                        if rule.check_constraints(self.events):
                            cap = self.capabilities[rule.target.uid]
                            print(f"[ENGINE] Permiso concedido para {cap.asset.uid}")
                            cap.execute()

                # --- Prohibition ---
                if isinstance(rule, Prohibition) and rule.target.uid == event.source_uid:
                    print(f"[ENGINE] Acción prohibida detectada en {event.source_uid}")
