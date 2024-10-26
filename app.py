from flask import Flask, render_template, Response
import cv2
import random

app = Flask(__name__)

# Compliments list
compliments = [
    "You have an amazing sense of style!",
    "Your smile could light up any room.",
    "You're incredibly talented!",
    "Your energy is contagious!",
    "You make everyone around you feel special.",
    "You have a heart of gold!",
    "You're truly a one-of-a-kind person!",
    "Your creativity is boundless!"
]

# Initialize the video capture
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Compliment flag and message
compliment_shown = False
current_compliment = ""

def generate_frames():
    global compliment_shown, current_compliment
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            # If a face is detected, display a compliment
            if len(faces) > 0 and not compliment_shown:
                current_compliment = random.choice(compliments)
                compliment_shown = True
            elif len(faces) == 0:
                compliment_shown = False

            # Draw rectangles around faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Encode frame for streaming
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('project5.html', compliment=current_compliment)

if __name__ == "__main__":
    app.run(debug=True)
