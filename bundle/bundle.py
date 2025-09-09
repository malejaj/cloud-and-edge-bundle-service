import base64
from time import time , sleep
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

# list to store active requests
active_requests = []


# --- Helpers ---
def log_request(endpoint: str, data: dict):
    """Log each incoming request to the bundle for monitoring and debugging."""
    req_info = {"endpoint": endpoint, "data": data}
    active_requests.append(req_info)


def load_image_as_base64(path: str) -> str:
    """Load an image from disk and encode it as base64 string."""
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


# --- Bundle Endpoints ---
@router.get("/get-bundle")
async def get_bundle():
    """Return metadata describing available bundle endpoints."""
    bundle = {
        "endpoint1": "decision",#policy  1 applied 
        "endpoint2": "identification",
        "endpoint3": "trajectory_planning",
        "endpoint4": "detection",#policy 2 applied
        "endpoint5": "decision-raw",
        "endpoint6": "detection-raw",
        "endpoint7": "save",
    }
    return bundle


@router.post("/identification")
async def read_root(request: Request):
    """Forward identification request to the cloud service."""
    data = await request.json()
    response = requests.post("http://cloud:8001/identification", json=data)
    return response.json() 


def identification(data):
    """Call the external cloud identification service synchronously."""
    response = requests.post("http://34.94.7.83:8001/identification", json=data) #Cloud IP
    try:
        response = response.json()
    except ValueError:
        response = {"error": "Answer not in JSON format", "status_code": response.status_code}
    return response


@router.post("/decision-raw")
async def read_root(request: Request):
    """Send raw decision request directly to the edge service."""
    data = await request.json()
    response = requests.post(Edge_url, json=data)
    return response.json()


@router.post("/decision")
async def decision(request: Request, background_tasks: BackgroundTasks):
    """Apply Policy1 for decision-making: validate request, process with edge, and log outcome."""
    manager = ODRLManager(odrl_file="Policy1.json")
    policy_obj = manager.build_policy()

    data = await request.json()
    log_request("decision", data)

    TargetPermission = policy_obj[0].rules[0].target
    TargetPermission.add_property(data)

    action = policy_obj[0].rules[0].action
    action.callback = process_with_edge
    response = action.execute(data)

    TargetDuty = policy_obj[0].rules[0].duty[0].target
    TargetDuty.add_property(response)

    pretty_print_policy(policy_obj)
    return response


def process_with_edge(data: dict):
    """Send data to edge, get decision, and forward instruction to the car."""
    try:
        response = requests.post(Edge_url, json=data)
        decision = response.json()
        return decision
    except Exception as e:
        return {"error": str(e)}


@router.post("/detection-raw")
async def detection(request: Request):
    """Perform raw detection: check distance and call identification if object detected."""
    data = await request.json()
    log_request("detection", data)

    distance = data.get("distance", 999)
    if distance < 20:  # Threshold for object detection
        default_img64 = load_image_as_base64("bundle/default.png")
        img = {"img": default_img64}
    else:
        default_img64 = load_image_as_base64("bundle/default.png")
        img = {"img": default_img64}
    
    response = identification(img)
    return response


@router.post("/detection")
async def detection(request: Request):
    """Apply Policy2 for detection: trigger identification if object is detected."""
    manager = ODRLManager(odrl_file="Policy2.json")
    policy_obj = manager.build_policy()
    data = await request.json()
    log_request("detection", data)

    distance = data.get("distance", 999)
    if distance < 20:  # Threshold for object detection
        event = {"event": "object_detected"}
        target = policy_obj[0].rules[0].target
        target.add_property(event)

        action = policy_obj[0].rules[0].action
        action.callback = trigger_identification

        pretty_print_policy(policy_obj)
        return action.execute(event, policy_obj)

    return {"status": "clear", "message": "No obstacle detected"}


def trigger_identification(event, policy_obj):
    """Trigger identification process using second rule in Policy2."""
    try:
        policy_obj = policy_obj[1]
        target = policy_obj.rules[0].target

        action = policy_obj.rules[0].action
    
        default_img64 = load_image_as_base64("bundle/default.png")
        img = {"img": default_img64} 
        target.add_property(img)

        action.callback = identification
        result = action.execute(img)
        return result

    except Exception as e:
        return {"error": str(e)}


@router.post('/trajectory_planning')
async def read_root(request: Request):
    """Forward trajectory planning request to the cloud and return generated map."""
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
    """Forward save request to the cloud service."""
    data = await request.json()
    response = requests.post("http://34.94.7.83:8001/save", json=data)
    return response.json()


@router.get("/active-requests")
async def get_active_requests():
    """Return all logged active requests for monitoring purposes."""
    return active_requests
