import json
from fastapi import FastAPI
import uvicorn
from bundle.bundle import router as bundle_router
from ODRL_framework.core.actions_registry import actions_registry
from ODRL_framework.core.validator import validate_odrl
from ODRL_framework.core.builder import build_objects_from_ordl
from ODRL_framework.core.ODRL_enforcer import ODRLEnforcer
import ODRL_framework.builder_init  
from ODRL_framework.core.registry import builder_registry
app = FastAPI()

#route to the bundle services
# Acción de prueba
def print_alert(target_id):
    print(f"[TEST] Política disparada para {target_id}")



app.include_router(bundle_router, prefix="/bundle")
@app.get("/get-bundle")
def get_bundle():
    bundle = {
        "api":"bundle",
        "endpoint1":"decision", 
        "endpoint2":"identification", 
        "endpoint3":"trajectory_planning",
        "endpoint4":"save",    
    }
    return bundle


if __name__ == "__main__":
    #uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    builder_registry.add("Storage", lambda data: ODRL_framework.builder_init.Storage(**data))

    print("Tipos registrados:", list(builder_registry.keys()))
    actions_registry.register("print_alert", print_alert)
    
    # Cargar JSON
with open("ODRL_framework/example_odrl.json", "r") as f:
    ordl_data = json.load(f)

# Construir objetos
objects = {}
for obj_name, obj_data in ordl_data["objects"].items():
    obj_type = obj_data["type"]
    objects[obj_name] = builder_registry.build(obj_type, obj_data)

print("Objetos construidos:", objects)

# Simular ejecución de políticas
for policy in ordl_data["policies"]:
    target = objects[policy["target"]]
    used_percent = (target.used_gb / target.capacity_gb) * 100
    if eval(f"{used_percent} {policy['condition']['operator']} {policy['condition']['value']}"):
        print(f"⚠ Política {policy['id']} activada → Ejecutando {policy['action']['function']}")
    # 1. Validar ORDL
    ordl = validate_odrl("example_odrl.json", "schema/odrl_schema.json")

    # 2. Construir objetos
    #objects = build_objects_from_ordl("example_odrl.json")

    # 3. Evaluar políticas
    #policies = ordl.get("policies", [])
    #enforcer = ODRLEnforcer(objects, policies)
    #results = enforcer.evaluate_policies()

    #print("Resultados:", results)
