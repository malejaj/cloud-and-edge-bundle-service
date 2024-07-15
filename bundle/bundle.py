from fastapi import Request
from fastapi import APIRouter
from fastapi.responses import FileResponse
import requests

router = APIRouter()


#request of bundle and endpoint to the bundle services
@router.get("/get-bundle")
async def read_root():
    bundle = {
        "endpoint1":"decison", 
        "endpoint2":"identification", 
        "endpoint3":"trajectory_planning",    
    }
    return bundle

#decision capacities endpoint
@router.post("/decision")
async def read_root(request: Request):
    data = await request.json()
    response = requests.post('http://[edge-server-ip]/decision', json=data)
    return response.json()

#identification capacities endpoint
@router.post("/identification")
async def read_root(request: Request):
    data = await request.json()
    response = requests.post("http://[cloud-server-ip]/identification", json=data)
    return response.json()  

#trajectory planning capacitie endpoint
@router.post('/trajectory_planning')
async def read_root(request: Request):
    data = await request.json() 
    response = requests.post('http://[cloud-server-ip]/trajectory_planning', json=data) 
    if response.status_code == 200:
        with open('map.html', 'wb') as f:
            f.write(response.content)
        return FileResponse('map.html', media_type='text/html', filename='map.html')
    else:
        return {"error": "Failed to fetch data from external service"}
