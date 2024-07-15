import numpy as np
import json
import requests
import base64
import time
import cv2

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
responses = []

def save_response_times_to_file(filename='cloud_edge2_response_latency.json'):
    with open(filename, 'w') as f:
        json.dump(responses, f)
    print(f'Temps de réponse sauvegardés dans {filename}')

def identification(responses_cloud, api, endpoint):
    i = 0
    response_data = []
    #while i < 100:
    while True:
        success, img = cap.read()
        _, buffer = cv2.imencode('.jpg', img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')

        data = {
            "img": img_base64
        }
        t1 = time.time()
        url = f'http://[bundle-server-ip]:8000/{api}/{endpoint}'
        response = requests.post(url=url, json=data)
        if response.status_code == 200 and response.json():
            response = response.json()
            box = response["box"]
            classId = response["classId"]
            cv2.rectangle(img, box, color=(0,255,0), thickness=2)
            cv2.putText(img, classId, (box[0]+10, box[1]+30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0),1)

            cv2.imshow("Output",img)
            cv2.waitKey(1)
        t2 = time.time()
        print('delay identification [cloud] = ', (t2 - t1) * 1000)
        response_data.append((t2 - t1) * 1000)
        i = i + 1
    #responses_cloud.append(response_data)
    #print(responses_cloud)
        