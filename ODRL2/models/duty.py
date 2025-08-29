from registry import register_class

@register_class
class Duty:
    def __init__(self, action, assignee):
        self.action = action
        self.assignee = assignee

    def __repr__(self):
        return f"<Duty action={self.action} assignee={self.assignee}>"
