from fastapi import Request
from fastapi import APIRouter
from fastapi.responses import FileResponse
import requests

router = APIRouter()


#request of bundle and endpoint to the bundle services
@router.get("/get-bundle")
async def read_root():
    bundle = {
        "endpoint1":"decision", 
        "endpoint2":"identification", 
        "endpoint3":"trajectory_planning",  
        "endpoint4":"save",  
    }
    return bundle

#decision capacities endpoint
@router.post("/decision")
async def read_root(request: Request):
    data = await request.json()
    response = requests.post('http://192.168.231.188:8002/decision', json=data)
    return response.json()

#identification capacities endpoint
@router.post("/identification")
async def read_root(request: Request):
    data = await request.json()
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
