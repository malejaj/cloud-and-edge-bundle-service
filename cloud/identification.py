import base64
import numpy as np
import cv2

classNames= []
classFile = 'coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

def identification(data):
    img_base64 = data.get('img')
    img_bytes = base64.b64decode(img_base64)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    classIds, confs, bbox = net.detect(img, confThreshold=0.5)

    response = {}
    if len(classIds) != 0:
        for classId, box in zip(classIds, bbox):
            print(box.tolist())
            response = {
                "classId":classNames[classId-1],
                "box":box.tolist()
            }
            return response
    return response
