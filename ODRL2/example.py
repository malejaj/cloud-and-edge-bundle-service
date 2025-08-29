# JSON estilo ODRL
from registry import build_object
from bundle.Model import Party,Permission,Policy,Prohibition,Target,Action, Rule
from pathlib import Path
policy_data = {
    "type": "Policy",
    "uid": "pol1",
    "rules": [
        {
            "type": "Permission",
            "uid": "perm1",
            "target": {"type": "Target", "uid": "cap2", "name": "Obstacle Detection"},
            "action": {"type": "Action", "name": "use"},
            "assignee": {"type": "Party", "uid": "veh1", "role": "assignee"}
        }
    ]
}
policy_data=  Path(__file__).parent / "example-odrl.json"


# Construir el objeto
policy_obj = build_object(policy_data)
print(policy_obj)
