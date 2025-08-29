import json
from bundle.Model import Policy, Rule, Duty, Action, Party, Target, Constraint

def build_policy_from_json(data: dict) -> Policy:
    rules = []
    # Verifica si es una politica con el type
    if data.get("type") == "Set": # TODO : Qué otros types pueden ser posibles para la politica?
        # detectar y guardar valores planos str
        plain_data = {}
        for key, value in data.items():
            if isinstance(value, str):
                plain_data[key] = value

        # Recorre permisos
        for perm_data in data.get("permission", []):
            assignee = Party(perm_data["assignee"])
            target = Target(perm_data["target"])
           






    #     # Duties
    #     duties = []
    #     for duty_data in perm_data.get("duty", []):
    #         duty_action = Action(duty_data["action"])
    #         duty_target = Target(duty_data["target"])
    #         informed = Party(duty_data.get("informedParty")) if duty_data.get("informedParty") else None
    #         informing = Party(duty_data.get("informingParty")) if duty_data.get("informingParty") else None
    #         duties.append(Duty("Duty", duty_target, duty_action, informed, informing))

    #     # Constraints
    #     constraints = []
    #     for c in perm_data.get("constraint", []):
    #         constraints.append(
    #             Constraint(c["leftOperand"], c["operator"], c["rightOperand"])
    #         )

    #     # Creamos la regla Permission
    #     rule = Rule(
    #         type="Permission",
    #         assignee=assignee,
    #         target=target,
    #         action=action,
    #         duty=duties,
    #         constraint=constraints,
    #     )
    #     rules.append(rule)

    # # Creamos la política
    # return Policy(uid=data["uid"], type=data["type"], rules=rules)
