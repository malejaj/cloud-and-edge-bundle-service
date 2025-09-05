from fastapi import FastAPI
from time import sleep
import uvicorn
#from identification import identification
from main import stop

app = FastAPI()

import webbrowser
import json


@app.post("/apply-instruction")
def apply_instruction(instruction: dict):
    """
    El bundle envía la instrucción final al carro.
    """
    vitesse = instruction.get("vitesse")
    if vitesse =="0":
        #px.stop()
        stop()
        return {"status": "Car stopped"}
    else:
        return {"status": f"Instruction applied: {vitesse}"}  
if __name__=='__main__':
    uvicorn.run("main:app",host="0.0.0.0",port = 4000,reload=True)