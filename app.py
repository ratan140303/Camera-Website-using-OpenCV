from flask import Flask, render_template, Response, request
import os
import cv2
import datetime


app = Flask(__name__)
capture = False

# def enhance_image(image):
#     # Increase resolution
#     scale_percent = 150  # percent of original size
#     width = int(image.shape[1] * scale_percent / 100)
#     height = int(image.shape[0] * scale_percent / 100)
#     dim = (width, height)
#     # Resize image
#     resized = cv2.resize(image, dim, interpolation=cv2.INTER_CUBIC)

#     # Reduce noise
#     denoised = cv2.GaussianBlur(resized, (5, 5), 0)

#     # Convert to YUV color space
#     yuv = cv2.cvtColor(denoised, cv2.COLOR_BGR2YUV)

#     # Apply CLAHE to the Y channel
#     clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
#     yuv[:, :, 0] = clahe.apply(yuv[:, :, 0])

#     # Convert back to BGR color space
#     enhanced = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)

#     return enhanced

def open_camera():
    global capture

    camera = cv2.VideoCapture(cv2.CAP_ANY)

    # Create the directory for storing data if it doesn't exist
    if not os.path.exists('static/Photos'):
        os.makedirs('static/photos')

    facecascade = cv2.CascadeClassifier("Cascades\haarcascade_frontalface_default.xml")
    
    while True:
        ret, frame = camera.read()
        if ret: 
            flipped_frame = cv2.flip(frame, 1)
            # Convert the frame to grayscale
            gray = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2GRAY)

            # Detect faces in the frame
            face_coordinates = facecascade.detectMultiScale(gray, 1.3, 4)

            for (a, b, w, h) in face_coordinates:
                # Draw a rectangle around the face
                cv2.rectangle(flipped_frame, (a, b), (a+w, b+h), (255, 0, 0), 2)

            if capture:
                capture = False  # Reset capture flag
                # enhanced_frame = enhance_image(flipped_frame)
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                img_name = f"static/photos/photo_{timestamp}.jpg"
                cv2.imwrite(img_name, flipped_frame)

            try:
                ret, buffer = cv2.imencode('.jpg', flipped_frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                print(f"Error in encoding frame: {e}")

        else:
            print('Failed to capture frame')
            break  
    camera.release()
        



# Home Page 
@app.route('/', methods=['GET', 'POST'])
def index():
    global capture
    if request.method == 'POST':
        if request.form.get('click') == 'Capture Photo':
            capture = True
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(open_camera(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run(debug=True)
