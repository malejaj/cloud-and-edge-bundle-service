from fastapi import FastAPI, Request
import uvicorn
from vitesse_decision import vitesse_decision

app = FastAPI()

@app.post("/decision")
def read_root(data: dict):
    instruction={
                  "vitesse":""
                }
    dist = data["front"]
    vitesse = data["vitesse"]
    instruction["vitesse"] = vitesse_decision(dist, vitesse)
    return instruction

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
