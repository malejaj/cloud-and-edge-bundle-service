from typing import List, Optional, Union
from bundle.registry import register_class


# ------------------------------
# Basic model elements
# ------------------------------

@register_class

class Target:
    def __init__(self, id: str):
        self.real_value = None
        self.id = id

    def __repr__(self):
        return f"Target(id='{self.id}', real_value='{self.real_value}')"
    def add_property(self, real_value: dict):
        self.real_value = real_value


@register_class
class Party:
    def __init__(self, id: str):
        self.id = id

    def __repr__(self):
        return f"Party(id='{self.id}')"


@register_class
class Action:
    def __init__(self, data: Union[str, dict]):
        self._callback = None  # internal callback
        self.real_value = None  # name

        if isinstance(data, str):
            self.id = data
            self.refinement = []
        elif isinstance(data, dict):
            self.id = data.get("id")
            self.refinement = data.get("refinement", [])
        else:
            raise ValueError(f"Invalid action data: {data}")

    @property
    def callback(self):
        return self._callback

    @callback.setter
    def callback(self, func):
        self._callback = func
        if func:
            self.real_value = func.__name__  # guarda el nombre de la función
        else:
            self.real_value = None

    def execute(self, *args, **kwargs):
        if self._callback:
            print(f"[ACTION] executing {self.id} with callback {self.real_value}")
            return self._callback(*args, **kwargs)
        else:
            print(f"[ACTION] No callback defined for {self.id}")
            return None

    def __repr__(self):
        return f"Action(id='{self.id}', refinement={self.refinement}, real_value='{self.real_value}')"

# ------------------------------
# Rules
# ------------------------------

class Rule:
    """Base class for any type of rule."""
    def __init__(self, uid: str, target: Target, action: Action,
                 assigner: Optional[Party] = None,
                 assignee: Optional[Party] = None,
                 constraints: Optional[List] = None):
        self.uid = uid
        self.target = target
        self.action = action
        self.assigner = assigner
        self.assignee = assignee
        self.constraints = constraints or []


    def check_constraints(self, context: dict):
        """Validate that all constraints are satisfied in a given context."""
        return all(c.is_satisfied(context) for c in self.constraints)

    def __repr__(self):
        return ("Rule(uid={uid}, target={target}, action={action}, assigner={assigner}, "
                "assignee={assignee}, constraints={constraints})".format(
                    uid=self.uid,
                    target=self.target,
                    action=self.action,
                    assigner=self.assigner,
                    assignee=self.assignee,
                    constraints=self.constraints
                ))


@register_class
class Permission(Rule):
    """Permission to perform an action on an Target."""
    def __init__(self, uid: str, target: Target, action: Action,
                 assigner: Optional[Party] = None,
                 assignee: Optional[Party] = None,
                 constraints: Optional[List] = None,rules: Optional[List] = None):
        self.uid = uid
        self.target = target
        self.action = action
        self.assigner = assigner
        self.assignee = assignee
        self.constraints = constraints or []
        self.rules = rules or []
            
    def __repr__(self):
        return ("Permission(uid={uid}, target={target}, action={action}, assigner={assigner}, "
                "assignee={assignee}, constraints={constraints}, rules={rules})".format(
                    uid=self.uid,
                    target=self.target,
                    action=self.action,
                    assigner=self.assigner,
                    assignee=self.assignee,
                    constraints=self.constraints,
                    rules=self.rules
                ))


@register_class
class Prohibition(Rule):
    """Prohibition to perform an action on an Target."""
    def __repr__(self):
        return ("Prohibition(uid={uid}, target={target}, action={action}, assigner={assigner}, "
                "assignee={assignee}, constraints={constraints})".format(
                    uid=self.uid,
                    target=self.target,
                    action=self.action,
                    assigner=self.assigner,
                    assignee=self.assignee,
                    constraints=self.constraints
                ))


@register_class
class Duty(Rule):
    """Obligation to perform an action on an Target."""
    def __repr__(self):
        return ("Duty(uid={uid}, target={target}, action={action}, assigner={assigner}, "
                "assignee={assignee}, constraints={constraints})".format(
                    uid=self.uid,
                    target=self.target,
                    action=self.action,
                    assigner=self.assigner,
                    assignee=self.assignee,
                    constraints=self.constraints
                ))


# ------------------------------
# Policies
# ------------------------------

@register_class
class Rule:
    """
    Generic rule Permission, Duty, Obligation, etc.
    """
    def __init__(self, type, assignee=None, target=None, action=None, duty=None, constraint=None,
                 informedParty=None, informingParty=None):
        self.type = type  # "Permission", "Duty", "Obligation", etc.
        self.assignee = assignee  # Party
        self.target = target      # Target
        self.action = action      # Action
        self.duty = duty or []    # Lista de Duty
        self.constraint = constraint or []  # Lista de Constraint
        self.informedParty = informedParty
        self.informingParty = informingParty

    def __repr__(self):
        return ("Rule(type={type}, assignee={assignee}, target={target}, action={action}, "
                "duty={duty}, constraint={constraint}, informedParty={informed}, informingParty={informing})".format(
                    type=self.type,
                    assignee=self.assignee,
                    target=self.target,
                    action=self.action,
                    duty=self.duty,
                    constraint=self.constraint,
                    informed=self.informedParty,
                    informing=self.informingParty
                ))

class Policy:
    def __init__(self, uid, type, rules=None):
        self.uid = uid
        self.type = type  # Normalmente "Set"
        self.rules = rules or []  # Lista de Rule
    def __repr__(self):
        return "Policy(uid={uid}, type={type}, rules={rules})".format(
            uid=self.uid, type=self.type, rules=self.rules
        )


@register_class
class Set(Policy):
    """A Policy of type 'Set' (as defined in ODRL)."""
    def __init__(self, uid: str, context: str, rules: List[Rule]):
        super().__init__(uid, context, rules)
    def __repr__(self):
        return "Set(uid={uid}, context={context}, rules={rules})".format(
            uid=self.uid, context=self.type, rules=self.rules
        )

@register_class
class Constraint:
    """Constraint on when/how a rule can be applied."""
    def __init__(self, leftOperand: str, operator: str, rightOperand: str):
        self.leftOperand = leftOperand
        self.operator = operator
        self.rightOperand = rightOperand

    def __repr__(self):
        return "Constraint(leftOperand={left}, operator={op}, rightOperand={right})".format(
            left=self.leftOperand, op=self.operator, right=self.rightOperand
        )