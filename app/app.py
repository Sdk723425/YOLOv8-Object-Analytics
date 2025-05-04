from flask import Flask, render_template, Response, request
import cv2
from ultralytics import YOLO
from utils.counter import RegionCounter
from utils.speed_estimator import SpeedEstimator
from utils.zones import load_zones

app = Flask(__name__)
model = YOLO('models/yolov8n.pt')
zones = load_zones('zones.json')
counter = RegionCounter(zones)
speed_estimator = SpeedEstimator()

cap = None

def generate_frames():
    global cap
    while True:
        success, frame = cap.read()
        if not success:
            break

        results = model.track(frame, persist=True, verbose=False)
        annotated_frame, object_data = counter.update(frame, results)
        speed_estimator.update(object_data)

        _, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/upload', methods=['POST'])
def upload():
    global cap
    file = request.files['video']
    if file:
        filepath = 'sample_videos/' + file.filename
        file.save(filepath)
        cap = cv2.VideoCapture(filepath)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
