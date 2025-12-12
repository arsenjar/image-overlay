import cv2 as cv
import cv2 as cv2
import numpy as np
from arseny import arsenyCode
from flask import Flask, Response, request, jsonify
from flask_cors import CORS 
from login import app
import time

app = Flask(__name__)
CORS(app)
HOST_IP = '0.0.0.0'
PORT = 8080 

camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_FPS, 30)

if not camera.isOpened():
    print("Error: Could not open camera.")

def cannyEdge(img):
    #img = cv2.imread(fileName)
    nImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #height, width, _ = img.shape
    #scale = 1 / 5
    #heightScale = int(height * scale)
    #widthScale = int(width * scale)
    #img = cv2.resize(img, (widthScale, heightScale), interpolation=cv2.INTER_LINEAR)
    canniedEdge = cv2.Canny(nImg, 255, 255)
    return canniedEdge
    

current_state = {
    'up': False,
    'down': False,
    'left': False,
    'right': False,
    'command': 'stop'
}

def generate_frames():
    while True:
        # Read the camera frame
        success, frame = camera.read()
        if not success:
            break

        (flag, encodedImage) = cv2.imencode(".jpg", frame)

        if not flag:
            continue

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + 
               bytearray(encodedImage) + b'\r\n')

def generateopenCVFrames():
    while True:
        success, frame = camera.read()
        if not success:
            break

        arsenyFrame = arsenyCode(frame)

        if arsenyFrame is None or arsenyFrame.size == 0:
            h, w = 480, 640
            arsenyFrame = np.zeros((h, w, 3), np.uint8)
            cv.putText(arsenyFrame, "FRAME ERROR", (100, 240), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 4)

        (flag, encodedImage) = cv2.imencode(".jpg", arsenyFrame)
        if not flag:
            continue

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + encodedImage.tobytes() + b'\r\n')

@app.route('/gui')
def gui():
    if session.get('logged_in'):
        return render_template('gui.html', username = session.get("username"))
    else:
        return redirect(url_for("index", message = "Log in first."))

@app.route('/video_feed')
def video_feed():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/video_feedUp')
def upvideo_feed():
    return Response(
         generateopenCVFrames(),
         mimetype='multipart/x-mixed-replace; boundary=frame'
    )
@app.route('/control/set', methods=['POST'])
def control_set():
    global current_state
    
    try:
        data = request.get_json()
        current_state.update(data)

        print(f"Received Command: {current_state['command']}, State: {data}")
        return jsonify({'status': 'success', 'state': current_state})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    print(f"Streaming server running on http://{HOST_IP}:{PORT}")
    try:
        app.run(host=HOST_IP, port=PORT, threaded=True)
    finally:
        # Release the camera resource when the server is stopped
        camera.release()
