import json
from fastapi import FastAPI
import uvicorn
from bundle.bundle import router as bundle_router

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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
   
    

