import cv2
import base64
import requests

cap = cv2.VideoCapture(0)

 
def main():

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    print("Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        _, buffer = cv2.imencode('.jpg', frame)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        data = {"img": img_base64}

        try:
            response = requests.post("http://localhost:8000/bundle/identification", json=data)
            print(f"Status: {response.status_code}")
            if response.status_code == 200 and response.json():
                result = response.json()
                classId = result["classId"]
                box = result["box"]
                print(f"Detected: {classId} at {box}")
                cv2.rectangle(frame, tuple(box), color=(0,255,0), thickness=2)
                cv2.putText(frame, classId, (box[0]+10, box[1]+30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 1)
        except Exception as e:
            print("Request failed:", e)

        cv2.imshow("Output", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

main()
