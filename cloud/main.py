from fastapi import FastAPI, Request
import uvicorn
from identification import identification
from trajectory import trajectory
from fastapi.responses import FileResponse, JSONResponse
import json

app = FastAPI()

#identification capacitie
@app.post("/identification")
async def read_root(request: Request):
    data = await request.json()
    response ="hola" # identification(data)
    return response

#trajectory planning capacitie
@app.post('/trajectory_planning')
async def read_root(request: Request):
    data = await request.json()
    start_address = data['start_address']
    end_address = data['end_address']
    folium_map = trajectory(start_address, end_address)
    map_file = 'map.html'
    folium_map.save(map_file)
    return FileResponse(map_file, media_type='file', filename=map_file)


@app.post('/save')
async def save_file(request: Request):
    data = await request.json()
    print("Received:", data) 
    file_path = 'data_save.json'
    
    with open(file_path, 'a') as f:
        json.dump(data, f)
        f.write('\n')
    
    return {"message": "File saved successfully", "file_path": file_path}
@app.get('/data')
async def read_saved_data():
    try:
        with open('data_save.json', 'r') as f:
            content = f.read()
        return JSONResponse(content=content)
    except FileNotFoundError:
        return {"error": "File not found"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)