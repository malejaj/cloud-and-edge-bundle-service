from picarx import Picarx
from fastapi import FastAPI
import requests
from time import sleep
import time
import threading
import requests
from identification import identification

app = FastAPI()

import webbrowser
import json

px = Picarx()

current_state = None
px_power = 10
offset = 20
last_state = "stop"
lock = threading.Lock()
responses = []
responses_cloud = []

#latency save
def save_response_times_to_file(filename='cloud_edge_response_latency.json'):
    with open(filename, 'w') as f:
        json.dump(responses, f)
    print(f'Temps de réponse sauvegardés dans {filename}')
    
def save_response_times2_to_file(filename='cloud_edge2_response_latency.json'):
    with open(filename, 'w') as f:
        json.dump(responses_cloud, f)
    print(f'Temps de réponse sauvegardés dans {filename}')


def outHandle():
    global last_state, current_state
    if last_state == 'left':
        px.set_dir_servo_angle(-30)
        px.backward(10)
    elif last_state == 'right':
        px.set_dir_servo_angle(30)
        px.backward(10)
    while True:
        gm_val_list = px.get_grayscale_data()
        gm_state = get_status(gm_val_list)
        currentSta = gm_state
        if currentSta != last_state:
            break
    sleep(0.001)

def get_status(val_list):
    _state = px.get_line_status(val_list)
    if _state == [0, 0, 0]:
        return 'stop'
    elif _state[1] == 1:
        return 'forward'
    elif _state[0] == 1:
        return 'right'
    elif _state[2] == 1:
        return 'left'

def circulation():
    try:
        while True:
        #i = 0
        #while i < 100:
            t1 = time.time()
            gm_val_list = px.get_grayscale_data()
            gm_state = get_status(gm_val_list)
            t2 = time.time()
            if gm_state != "stop":
                last_state = gm_state

            if gm_state == 'forward':
                px.set_dir_servo_angle(0)
                px.forward(px_power)
            elif gm_state == 'left':
                px.set_dir_servo_angle(offset)
                px.forward(px_power)
            elif gm_state == 'right':
                px.set_dir_servo_angle(-offset)
                px.forward(px_power)
            else:
                outHandle()
            #i += 1
    finally:
        px.stop()
        print("stop and exit")
        sleep(0.1)

def detection(api, endpoint):
    global px_power
    i = 0
    response_data = []
    while True:
    #while i < 100:
        ultrasonic_percept = px.ultrasonic.read()
        data = {
            "front":ultrasonic_percept,
            "vitesse":px_power
            }
        t1 = time.time()
        url = f'http://[bundle-server-ip]:8000/{api}/{endpoint}'
        response = requests.post(url=url, json=data)
        t2 = time.time()
        response_data.append((t2 - t1) * 1000)
        print('latency detection [edge] = ', (t2 - t1) * 1000)
        with lock:
            px_power = response.json()["vitesse"]
        #i = i + 1
    #responses.append(response_data)
    #save_response_times_to_file()

@app.post("/apply-instruction")
def apply_instruction(instruction: dict):
    """
    El bundle envía la instrucción final al carro.
    """
    vitesse = instruction.get("vitesse")
    if vitesse == "stop":
        px_power.stop()
        return {"status": "Car stopped"}
    else:
        # aquí puedes manejar seguir o cambiar velocidad
        return {"status": f"Instruction applied: {vitesse}"}  
    
def trajectory_planning(api, endpoint):
    data = {
            "start_address":"Tripode A",
            "end_address":"7 avenue colonel roche"
        }
    url = f'http://[bundle-server-ip]:8000/{api}/{endpoint}'
    response = requests.post(url=url, json=data)
    if response.status_code == 200:
        with open("received_map.html", "wb") as f:
            f.write(response.content)
        print("Map saved as received_map.html")
        webbrowser.open("received_map.html")
    else:
        print(f"Failed to retrieve map: {response.status_code} - {response.text}")
    
if __name__=='__main__':
    
    reponse = requests.get(url="http://[bundle-server-ip]:8000/get-bundle")
    data = reponse.json()
    t1 = time.time()
    trajectory_planning(data['api'], data['endpoint3'])
    t2 = time.time()
    print('delay trajectory [cloud] = ', (t2 - t1) * 1000)
    i = 0
#while i < 10:       
    thread1 = threading.Thread(target=circulation)
    thread2 = threading.Thread(target=detection, args=(data['api'], data['endpoint1'],))
    thread3 = threading.Thread(target=identification, args=(responses_cloud, data['api'], data['endpoint2'], ))

    thread1.start()
    thread2.start()
    thread3.start()
    
    thread1.join()
    thread2.join()
    thread3.join()
    #i += 1
#save_response_times_to_file()
#save_response_times2_to_file()
