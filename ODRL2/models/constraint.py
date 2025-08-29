from registry import register_class

@register_class
class Constraint:
    def __init__(self, leftOperand, operator, rightOperand):
        self.leftOperand = leftOperand
        self.operator = operator
        self.rightOperand = rightOperand

    def __repr__(self):
        return (f"<Constraint {self.leftOperand} {self.operator} {self.rightOperand}>")

    def is_satisfied(self, context):
        """
        context: dict con valores para comparar, ej: {'distance': 25}
        """
        val = context.get(self.leftOperand)
        if val is None:
            return False

        if self.operator == "lteq":
            return val <= self.rightOperand
        elif self.operator == "lt":
            return val < self.rightOperand
        elif self.operator == "gteq":
            return val >= self.rightOperand
        elif self.operator == "gt":
            return val > self.rightOperand
        elif self.operator == "eq":
            return val == self.rightOperand
        else:
            raise ValueError(f"Operador desconocido: {self.operator}")
