import json
from bundle.Model import Policy, Rule, Action, Party, Target, Constraint

def build_policy_from_json(data: dict) -> list[Policy]:
    policies = []
    for item in data:
        rules: list[Rule] = []
        if item.get("type") != "Set":
            continue

        plain_data = {k: v for k, v in item.items() if isinstance(v, str)}

        def build_action(a_data):
            if a_data is None:
                return None
            return Action(a_data)

        def build_target(t_data):
            if t_data is None:
                return None
            return Target(t_data)

        def build_party(p_data):
            if p_data is None:
                return None
            return Party(p_data)

        def build_constraints(constraint_list):
            built = []
            for c in constraint_list or []:
                if not isinstance(c, dict):
                    continue
                right_operand = c.get("rightOperand")
                if isinstance(right_operand, dict) and "@id" in right_operand:
                    right_operand = right_operand["@id"]
                left = c.get("leftOperand")
                op = c.get("operator")
                if left and op is not None:
                    built.append(Constraint(left, op, right_operand))
            return built

        def build_rule(rdata: dict, rule_type: str) -> Rule:
            assignee = build_party(rdata.get("assignee"))
            target = build_target(rdata.get("target"))
            action = build_action(rdata.get("action"))
            constraints = build_constraints(rdata.get("constraint"))
            informed = build_party(rdata.get("informedParty"))
            informing = build_party(rdata.get("informingParty"))
            # Recursión para duties (y potencialmente otros tipos si anidan en el futuro)
            nested_duties = [build_rule(d, "duty") for d in rdata.get("duty", [])]
            return Rule(
                type=rule_type,
                assignee=assignee,
                target=target,
                action=action,
                duty=nested_duties,
                constraint=constraints,
                informedParty=informed,
                informingParty=informing,
            )

        # Construir reglas de primer nivel (permission, prohibition, duty)
        for rule_type in ("permission", "prohibition", "duty"):
            for rdata in item.get(rule_type, []):
                rules.append(build_rule(rdata, rule_type))

        policy = Policy(uid=plain_data.get("uid"), type=plain_data.get("type"), rules=rules)
        policies.append(policy)

    return policies

