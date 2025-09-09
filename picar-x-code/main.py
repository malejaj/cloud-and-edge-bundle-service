from picarx import Picarx
from fastapi import FastAPI
import requests
from time import sleep
import time
import threading
import requests
import uvicorn

app = FastAPI()

import webbrowser
import json

px = None

current_state = None
px_power = 10
offset = 20
last_state = "stop"
lock = threading.Lock()
responses_edge = []
responses_cloud = []

bundleIP = "140.93.97.159"
port = 8000
iter = 100
iter1 = 7


# --- Helpers to save response times ---
# Change here to save in a different file
def save_response_times_to_file(filename='Edge.json'):#*edgeP
    """Save latency results for Edge responses into JSON file."""
    with open(filename, 'w') as f:
        json.dump(responses_edge, f)


def save_response_times2_to_file(filename='Cloud.json'):#*cloudP
    """Save latency results for Cloud responses into JSON file."""
    with open(filename, 'w') as f:
        json.dump(responses_cloud, f)


# --- Car control functions ---
def outHandle():
    """Handle car state transitions when line following is lost."""
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
    """Return current driving state based on grayscale sensor values."""
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
    """Control main circulation logic: follow line and adjust direction."""
    try:
        while True:
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
    finally:
        px.stop()
        sleep(0.1)


# --- Bundle interactions ---
def decision(api, endpoint):
    """Send decision request to bundle and update car speed accordingly."""
    global px_power
    i = 0
    response_data = []
    while i < iter1:
        ultrasonic_percept = px.ultrasonic.read()
        data = {
            "front": ultrasonic_percept,
            "vitesse": px_power
        }
        t1 = time.time()
        url = f'http://{bundleIP}:{8000}/{api}/{endpoint}'
        response = requests.post(url=url, json=data, timeout=5)
        t2 = time.time()
        response_data.append(f"{(t2 - t1) * 1000:.3f}")
        
        with lock:
            px_power = response.json()["vitesse"]
           
        i = i + 1
        
    responses_edge.append(response_data)


def stop():
    """Stop the car."""
    px.stop()


def trajectory_planning(api, endpoint):
    """Request a trajectory plan from the cloud and save map locally."""
    data = {
        "start_address": "Tripode A",
        "end_address": "7 avenue colonel roche"
    }
    url = f'http://{bundleIP}:{8000}/{api}/{endpoint}'
    response = requests.post(url=url, json=data)
    if response.status_code == 200:
        with open("received_map.html", "wb") as f:
            f.write(response.content)
        webbrowser.open("received_map.html")


def identification(api, endpoint):
    """Send identification request to cloud with ultrasonic data."""
    # if camera's car is available, send image and ultrasonic data 
    global px_power
    i = 0
    response_data = []
    while i < iter1:
        ultrasonic_percept = px.ultrasonic.read()
        data = {
            "distance": ultrasonic_percept
        }
        t1 = time.time()
        url = f'http://{bundleIP}:{8000}/{api}/{endpoint}'
        response = requests.post(url=url, json=data, timeout=7)
        if response.status_code == 200 and response.json():
            response = response.json()
            t2 = time.time()
        response_data.append(f"{(t2 - t1) * 1000:.3f}")
        i = i + 1
    responses_cloud.append(response_data)


def get_px():
    """Initialize and return Picarx instance if not already created."""
    global px
    if px is None:
        px = Picarx()
    return px


# --- Main execution ---
if __name__ == '__main__':
    px = get_px()
    reponse = requests.get(url=f"http://{bundleIP}:{port}/get-bundle")
    data = reponse.json()
    t1 = time.time()
    trajectory_planning(data['api'], data['endpoint3'])
    t2 = time.time()
    print('delay trajectory [cloud] = ', (t2 - t1) * 1000)
 
    for i in range(iter):
        thread1 = threading.Thread(target=circulation)
        thread2 = threading.Thread(target=decision, args=(data['api'], data['endpoint5'],))
        thread3 = threading.Thread(target=identification, args=(data['api'], data['endpoint6'],))
        # endpoint 5 and 6 to use policy 1 and 2 respectively
        # endpoint 1 and 4 to dont use policies

        thread1.start()
        thread2.start()
        thread3.start()

        thread1.join()
        thread2.join()
        thread3.join()
        print("iteration ", i)

    save_response_times_to_file()
    save_response_times2_to_file()
    px.stop()