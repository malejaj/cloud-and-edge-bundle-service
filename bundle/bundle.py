from time import time
from fastapi import Request ,BackgroundTasks
from fastapi import APIRouter
from fastapi.responses import FileResponse
import requests
from bundle.ODRLmanager import ODRLManager, pretty_print_policy
from bundle.Model import *


router = APIRouter()
Edge_url = "http://localhost:8002/decision"
Car_url = "http://localhost:8000/active-requests"
# Lista global para guardar peticiones activas
active_requests = []

# --- Helpers ---
def log_request(endpoint: str, data: dict):
    """Store each incoming request to the bundle."""
    req_info = {"endpoint": endpoint, "data": data}
    active_requests.append(req_info)
    #print(f"[BUNDLE] Logged request on '{endpoint}' with data: {data}")


# --- Bundle Endpoints ---
@router.get("/get-bundle")
async def get_bundle():
    bundle = {
        "endpoint1": "decision",
        "endpoint2": "identification",
        "endpoint3": "trajectory_planning",
        "endpoint4": "save",
    }
    print("[BUNDLE] Bundle metadata requested.")
    return bundle


@router.post("/decision")
async def decision(request: Request, background_tasks: BackgroundTasks):
    """Main decision endpoint of the bundle."""
    manager = ODRLManager()
    policy_obj = manager.build_policy()

    data = await request.json()
    log_request("decision", data)

    # Update target of the permission
    TargetPermission = policy_obj[0].rules[0].target
    TargetPermission.add_property(data)

    # Assign the processing function to the policy action
    action = policy_obj[0].rules[0].action
    action.callback = process_with_edge
    action.execute(data)

    response = {"status": "ok", "message": "Data received and processed with edge."}

    # Update duty target
    TargetDuty = policy_obj[0].rules[0].duty[0].target
    TargetDuty.add_property(response)

    print("[BUNDLE] Current Policy:")
    pretty_print_policy(policy_obj)
    return response


# --- Processing ---
def process_with_edge(data: dict):
    """
    1. Send data to the edge.
    2. Get decision from edge.
    3. Forward instruction to the car.
    """
    try:
        print("[BUNDLE] Sending data to edge...")
        response = requests.post(Edge_url, json=data, timeout=3)
        decision = response.json()
        print(f"[BUNDLE] Edge decision received: {decision}")

        print("[BUNDLE] Forwarding decision to car...")
        requests.post(Car_url, json=decision, timeout=3)
        print("[BUNDLE] Instruction sent to car successfully.")

        return decision
    except Exception as e:
        print(f"[BUNDLE] Error while processing with edge: {e}")
        return {"error": str(e)}


#identification capacities endpoint
@router.post("/identification")
async def read_root(request: Request):
    manager = ODRLManager(odrl_file="Policy2.json")
    policy_obj = manager.build_policy()
    print("policy_obj:", policy_obj)
    data = await request.json()
    log_request("identification", data)
    response = requests.post("http://localhost:8001/identification", json=data)
    return response.json()  

#trajectory planning capacitie endpoint
@router.post('/trajectory_planning')
async def read_root(request: Request):
    data = await request.json() 
    response = requests.post('http://cloud:8001/trajectory_planning', json=data) 
    if response.status_code == 200:
        with open('map.html', 'wb') as f:
            f.write(response.content)
        return FileResponse('map.html', media_type='text/html', filename='map.html')
    else:
        return {"error": "Failed to fetch data from external service"}
    
@router.post("/save")
async def read_root(request: Request):
    data = await request.json()
    response = requests.post("http://localhost:8001/save", json=data)
    return response.json()


# Endpoint para consultar las peticiones registradas
@router.get("/active-requests")
async def get_active_requests():
    return active_requests