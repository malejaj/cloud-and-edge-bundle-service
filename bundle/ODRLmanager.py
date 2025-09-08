import json
from pathlib import Path

from bundle.validator import validate_ordl
from bundle.builder2 import build_policy_from_json
from bundle.Model import Policy


class ODRLManager:
    """Class to manage ODRL policies."""

    def __init__(self, odrl_file="Policy1.json", schema_file="ordl_schema.json"):
        base_path = Path(__file__).parent
        self.odrl_path = base_path / odrl_file
        self.schema_path = base_path / schema_file
        self.policy_obj: list[Policy] = []

    def load_policy(self) -> dict:
        """Load the JSON policy from file."""
        with open(self.odrl_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def validate_policy(self) -> None:
        """Validate the JSON against the ODRL schema."""
        validate_ordl(self.odrl_path, self.schema_path)

    def build_policy(self) -> list[Policy]:
        """Convert the JSON policy into Python objects."""
        policy_data = self.load_policy()
        self.validate_policy()
        self.policy_obj = build_policy_from_json(policy_data)
        return self.policy_obj

    def get_policy(self) -> list[Policy]:
        """Return the Policy object already built."""
        if not self.policy_obj:
            self.build_policy()
        return self.policy_obj


def pretty_print_policy(policy_obj, indent=0):
    """Print an ODRL policy in a readable and hierarchical way."""
    space = "  " * indent
    out = ""

    if isinstance(policy_obj, list):
        for p in policy_obj:
            out += pretty_print_policy(p, indent)
        return out

    # Policy
    out += f"{space}Policy:\n"
    out += f"{space}  UID: {policy_obj.uid}\n"
    out += f"{space}  Type: {policy_obj.type}\n"

    for rule in policy_obj.rules:
        out += f"{space}  Rule ({rule.type}):\n"
        if rule.assignee:
            out += f"{space}    Assignee: {rule.assignee.id}\n"
        if rule.target:
            out += f"{space}    Target: {rule.target}\n"
        if rule.action:
            out += f"{space}    Action: {rule.action}\n"
            if rule.action.refinement:
                out += f"{space}      Refinement: {rule.action.refinement}\n"

        # Duty
        if rule.duty:
            out += f"{space}    Duties:\n"
            for d in rule.duty:
                out += f"{space}      Duty:\n"
                if d.action:
                    out += f"{space}        Action: {d.action}\n"
                    if d.action.refinement:
                        out += f"{space}          Refinement: {d.action.refinement}\n"
                #if d.target:
                    #out += f"{space}        Target: {d.target}\n"
                if d.informedParty:
                    out += f"{space}        Informed Party: {d.informedParty}\n"
                if d.informingParty:
                    out += f"{space}        Informing Party: {d.informingParty}\n"

        # Constraint
        if rule.constraint:
            out += f"{space}    Constraints:\n"
            for c in rule.constraint:
                out += f"{space}      - {c.leftOperand} {c.operator} {c.rightOperand}\n"

    return out
