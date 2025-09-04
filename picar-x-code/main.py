from picarx import Picarx
from fastapi import FastAPI
import requests
from time import sleep
import time
import threading
import requests
import uvicorn
#from identification import identification

app = FastAPI()

import webbrowser
import json

px = None



current_state = None
px_power = 10
offset = 20
last_state = "stop"
lock = threading.Lock()
responses = []
responses_cloud = []

bundleIP="140.93.97.159"
port = 8000
iter =40

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





def decision(api, endpoint):
    global px_power
    i = 0
    response_data = []
    #for i in range(iter):
    #while i < 100:
    ultrasonic_percept = px.ultrasonic.read()
    data = {
        "front":ultrasonic_percept,
        "vitesse":px_power
        }
    t1 = time.time()
    url = f'http://{bundleIP}:{8000}/{api}/{endpoint}'
    response = requests.post(url=url, json=data)
    t2 = time.time()
    response_data.append((t2 - t1) * 1000)
    #print(response.json())
    print('latency detection [edge] = ', (t2 - t1) * 1000)
    with lock:
        px_power = response.json()
        print("vitesse", px_power)
    #i = i + 1
    responses.append(response_data)
def stop():
    px.stop()
    
def trajectory_planning(api, endpoint):
    data = {
            "start_address":"Tripode A",
            "end_address":"7 avenue colonel roche"
        }
    url = f'http://{bundleIP}:{8000}/{api}/{endpoint}'
    response = requests.post(url=url, json=data)
    if response.status_code == 200:
        with open("received_map.html", "wb") as f:
            f.write(response.content)
        print("Map saved as received_map.html")
        webbrowser.open("received_map.html")
    else:
        print(f"Failed to retrieve map: {response.status_code} - {response.text}")
    


def identification(api,endpoint):
    global px_power
    i = 0
    response_data = []
    #while True:
    #while i < 100:
    ultrasonic_percept = px.ultrasonic.read()
    data = {
        "distance":ultrasonic_percept
    }
    #print("identification" , data)
    t1 = time.time()
    url =f'http://{bundleIP}:{8000}/{api}/{endpoint}'
    response = requests.post(url=url, json=data)
    #print(response.json())
    if response.status_code == 200 and response.json():
        response = response.json()
        #print(response.json())
        #classId = response["classId"]
        t2 = time.time()
        print('delay identification [cloud] = ', (t2 - t1) * 1000)
        response_data.append((t2 - t1) * 1000)
        #i = i + 1
    responses_cloud.append(response_data)

def get_px():
    global px
    if px is None:
        px = Picarx()
    return px


if __name__=='__main__':
   

    px = get_px()
    reponse = requests.get(url=f"http://{bundleIP}:{port}/get-bundle")
    data = reponse.json()
    t1 = time.time()
    trajectory_planning(data['api'], data['endpoint3'])
    t2 = time.time()
    print('delay trajectory [cloud] = ', (t2 - t1) * 1000)
 
    
    for i in range(10):
        #thread1 = threading.Thread(target=circulation)
        thread2 = threading.Thread(target=decision, args=(data['api'], data['endpoint1'],))
        thread3 = threading.Thread(target=identification, args=(data['api'], data['endpoint4'],))

        #thread1.start()
        thread2.start()
        thread3.start()

        #thread1.join()
        thread2.join()
        thread3.join()

    save_response_times_to_file()
    save_response_times2_to_file()
    '''
      decision(data['api'], data['endpoint1'])
        save_response_times_to_file()
    print("hola")
    for i in range(10):
        decision(data['api'], data['endpoint5'])
        save_response_times_to_file()
        '''