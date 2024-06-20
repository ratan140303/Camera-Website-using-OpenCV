from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

def get_camera():
    # Example GStreamer pipeline to capture from /dev/video0
    gst_str = (
        'v4l2src device=/dev/video0 ! '
        'video/x-raw, width=640, height=480 ! '
        'videoconvert ! appsink'
    )

    # Create capture object
    camera = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

    # Check if camera opened successfully
    if not camera.isOpened():
        print("Error: Failed to open camera using GStreamer.")
    return camera

camera = get_camera()

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            print("Error: Failed to capture frame.")
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
