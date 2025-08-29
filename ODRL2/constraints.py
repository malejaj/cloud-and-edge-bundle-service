from typing import Any, Callable, Dict, List, Optional

# constraints.py
# Framework for ODRL (Open Digital Rights Language) policy constraints


class Constraint:
    """
    Represents a generic ODRL constraint.
    """
    def __init__(self, left_operand: str, operator: str, right_operand: Any):
        self.left_operand = left_operand
        self.operator = operator
        self.right_operand = right_operand

    def evaluate(self, context: Dict[str, Any]) -> bool:
        """
        Evaluates the constraint against the provided context.
        """
        value = context.get(self.left_operand)
        return self._apply_operator(value, self.operator, self.right_operand)

    def _apply_operator(self, value: Any, operator: str, right_operand: Any) -> bool:
        """
        Applies the operator to the value and right_operand.
        """
        if operator == 'eq':
            return value == right_operand
        elif operator == 'neq':
            return value != right_operand
        elif operator == 'gt':
            return value > right_operand
        elif operator == 'gte':
            return value >= right_operand
        elif operator == 'lt':
            return value < right_operand
        elif operator == 'lte':
            return value <= right_operand
        elif operator == 'in':
            return value in right_operand
        elif operator == 'nin':
            return value not in right_operand
        else:
            raise ValueError(f"Unsupported operator: {operator}")

class PolicyConstraints:
    """
    Manages a set of constraints for an ODRL policy.
    """
    def __init__(self, constraints: Optional[List[Constraint]] = None):
        self.constraints = constraints or []

    def add_constraint(self, constraint: Constraint):
        self.constraints.append(constraint)

    def evaluate_all(self, context: Dict[str, Any]) -> bool:
        """
        Evaluates all constraints against the provided context.
        Returns True if all constraints are satisfied.
        """
        return all(constraint.evaluate(context) for constraint in self.constraints)