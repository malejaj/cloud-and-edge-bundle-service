import base64
from time import time
from urllib import response
from fastapi import Request ,BackgroundTasks
from fastapi import APIRouter
from fastapi.responses import FileResponse
import requests
from bundle.ODRLmanager import ODRLManager, pretty_print_policy
from bundle.Model import *
from bundle.testCamara import capture_image

router = APIRouter()
Edge_url = "http://localhost:8002/decision"
Car_url = "http://140.93.64.105:4000/apply-instruction"
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
        "endpoint4": "detection",
        "endpoint5": "decision-raw",
        "endpoint6": "detection-raw",
        "endpoint7": "save",
    }
    print("[BUNDLE] Bundle metadata requested.")
    return bundle



@router.post("/decision-raw")
async def read_root(request: Request):
    data = await request.json()
    response = requests.post(Edge_url, json=data)
    return response.json()


@router.post("/decision")
async def decision(request: Request, background_tasks: BackgroundTasks):
    """Main decision endpoint of the bundle."""
    start = time()
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
    response = action.execute(data)

    TargetDuty = policy_obj[0].rules[0].duty[0].target
    TargetDuty.add_property(response)

    print("[BUNDLE] Current Policy:")
    pretty_print_policy(policy_obj)
    print(f"[decision-raw] POST to Edge took {time() - start:.3f}s")
    return response


# --- Processing ---
def process_with_edge(data: dict):
    """
    1. Send data to the edge.
    2. Get decision from edge.
    3. Forward instruction to the car.
    """
    try:
        response = requests.post(Edge_url, json=data)
        decision = response.json()
        print(f"[BUNDLE] Edge decision received: {decision}")

        print("[BUNDLE] Forwarding decision to car...")
      
        print("[BUNDLE] Instruction sent to car successfully.")

        return decision
    except Exception as e:
        print(f"[BUNDLE] Error while processing with edge: {e}")
        return {"error": str(e)}
# --- Identification capacity endpoint ---
@router.post("/identification")
async def read_root(request: Request):
    """
    Identification endpoint.
    Receives an image (base64) and executes the identification capacity 
    through the ODRL policy.
    """
    print("\n[IDENTIFICATION] --- New request received ---")

    # Load policy
    manager = ODRLManager(odrl_file="Policy2.json")
    policy_obj = manager.build_policy()
    print("[IDENTIFICATION] Policy loaded.")

    # Get request data
    data = await request.json()
    print("[IDENTIFICATION] Input data received:", data.keys())

    # Update policy target with input data
    target = policy_obj[0].rules[0].target
    target.add_property(data)
    print("[IDENTIFICATION] Target updated with request data.")

    # Define action callback = identification function
    action = policy_obj[0].rules[0].action
    action.callback = identification
    print("[IDENTIFICATION] Action callback set.")

    # Log request
    log_request("identification", data)

    # Execute action
    result = action.execute(data)
    print("[IDENTIFICATION] Action executed. Result:", result)

    # Print complete policy object for debugging
    print("\n[IDENTIFICATION] Current Policy Object:")
    print(policy_obj)

    return result


def identification(data):
    """
    Call the external identification service (Cloud).
    """
    print("[ACTION] Executing identification with external service...")
    response = requests.post("http://34.94.7.83:8001/identification", json=data)
    print("[ACTION] Identification response received.")     
    try:
        response = response.json()
    except ValueError:
        print("Respuesta no es JSON:", response.text)
        response = {"error": "Respuesta no es JSON", "status_code": response.status_code}

    return response


# --- Detection capacity endpoint ---
@router.post("/detection")
async def detection(request: Request):

    print("\n[DETECTION] --- New detection request received ---")

    # Load policy
    manager = ODRLManager(odrl_file="Policy2.json")
    policy_obj = manager.build_policy()
    print("[DETECTION] Policy loaded.")

    # Get request data (e.g., {"distance": 12})
    data = await request.json()
    print("[DETECTION] Input data:", data)

    # Log request
    log_request("detection", data)

    # Extract distance from data
    distance = data.get("distance", 999)
    if distance < 20:  # Threshold for object detection
        print("[DETECTION] Object detected at distance:", distance)

        # Trigger event
        event = {"event": "object_detected"}
        target = policy_obj[0].rules[0].target
        target.add_property(event)

        action = policy_obj[0].rules[0].action
        action.callback = trigger_identification
        print("[DETECTION] Event triggered: object_detected")

        # Debug: print the second policy in list
        print("[DETECTION] Related Policy:", pretty_print_policy(policy_obj))

        return action.execute(event, policy_obj)

    print("[DETECTION] No object detected. Distance =", distance)
  
    return {"status": "clear", "message": "No obstacle detected"}


def load_image_as_base64(path: str) -> str:
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")





@router.post("/detection-raw")
async def detection(request: Request):

    # Get request data (e.g., {"distance": 12})
    data = await request.json()
    print("[DETECTION-raw] Input data:", data)

    # Log request
    log_request("detection", data)

    # Extract distance from data
    distance = data.get("distance", 999)
    if distance < 20:  # Threshold for object detection
        print("[DETECTION] Object detected at distance:", distance)
        t1 = time()
        #img = capture_image()
        default_img64 = load_image_as_base64("bundle/default.jpg")
        img = default_img64
        t2 = time()
        print(f"[DETECTION-raw] Image captured in {t2 - t1:.2f} seconds.")
    else :
        # Ejemplo: usar imagen subida
        default_img64 = load_image_as_base64("default.jpg")
        img = default_img64

    response = identification(img)
    print("[DETECTION-raw] Identification result:", response)
    return response

    #return {"status": "clear", "message": "No obstacle detected"}


def trigger_identification(event, policy_obj):
 
    print("\n[TRIGGER] Triggering identification...")

    try:
        # Use the second policy (index 1) for identification
        policy_obj = policy_obj[1]
        target = policy_obj.rules[0].target

        # Get action from policy
        action = policy_obj.rules[0].action
        print("[TRIGGER] Action retrieved from policy:", action)
        t1 = time()
        # Capture an image for identification
        #img = capture_image()

        default_img64 = load_image_as_base64("bundle/default.jpg")
        img = default_img64
        # Update policy target with image
        target.add_property(img)
        print("[TRIGGER] Image captured.")

        # Assign callback to identificatio
        action.callback = identification
        print("[TRIGGER] Callback set to identification.")

        # Execute action
        result = action.execute(img)
        print("[TRIGGER] Identification executed. Result:", result)

        # Print complete policy object for debugging
        print("\n[TRIGGER] Current Policy Object:")
        #print(pretty_print_policy(policy_obj))

        return result

    except Exception as e:
        print(f"[TRIGGER] Error triggering identification: {e}")
        return {"error": str(e)}


#trajectory planning capacitie endpoint
@router.post('/trajectory_planning')
async def read_root(request: Request):
    data = await request.json() 
    response = requests.post('http://34.94.7.83:8001/trajectory_planning', json=data) 
    if response.status_code == 200:
        with open('map.html', 'wb') as f:
            f.write(response.content)
        return FileResponse('map.html', media_type='text/html', filename='map.html')
    else:
        return {"error": "Failed to fetch data from external service"}
    
@router.post("/save")
async def read_root(request: Request):
    data = await request.json()
    response = requests.post("http://34.94.7.83:8001/save", json=data)
    return response.json()


# Endpoint para consultar las peticiones registradas
@router.get("/active-requests")
async def get_active_requests():
    return active_requests