import cv2
import os
from flask import Flask, request, render_template
from datetime import date, datetime
import numpy as np
import pandas as pd
import face_recognition

# ================== Configuration ==================
app = Flask(__name__)

# Set your mobile camera IP here
MOBILE_CAM_IP = "http://192.168.124.9:8080/video"

# Date formats
datetoday = date.today().strftime("%m_%d_%y")
datetoday2 = date.today().strftime("%d-%B-%Y")

# Face Detector
face_detector = cv2.CascadeClassifier('static/haarcascade_frontalface_default.xml')

# Ensure necessary directories
os.makedirs('Attendance', exist_ok=True)
os.makedirs('static/faces', exist_ok=True)

# Attendance file creation
attendance_file = f'Attendance/Attendance-{datetoday}.csv'
if not os.path.exists(attendance_file):
    with open(attendance_file, 'w') as f:
        f.write('Name,Roll,Time\n')

# ================== Helper Functions ==================

def totalreg():
    return len(os.listdir('static/faces'))

def extract_faces(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_points = face_detector.detectMultiScale(gray, 1.3, 5)
    return face_points

def encode_known_faces():
    known_encodings, known_names = [], []
    for user in os.listdir('static/faces'):
        for imgname in os.listdir(f'static/faces/{user}'):
            img_path = f'static/faces/{user}/{imgname}'
            image = face_recognition.load_image_file(img_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(user)
    return known_encodings, known_names

def extract_attendance():
    if not os.path.exists(attendance_file) or os.path.getsize(attendance_file) == 0:
        return [], [], [], 0
    df = pd.read_csv(attendance_file)
    if 'Name' in df.columns and 'Roll' in df.columns and 'Time' in df.columns:
        return df['Name'], df['Roll'], df['Time'], len(df)
    return [], [], [], 0

def add_attendance(name):
    username, userid = name.split('_')
    current_time = datetime.now().strftime("%H:%M:%S")
    df = pd.read_csv(attendance_file)
    if 'Roll' not in df.columns or int(userid) not in df['Roll'].values:
        with open(attendance_file, 'a') as f:
            f.write(f'{username},{userid},{current_time}\n')

# ================== Flask Routes ==================

@app.route('/')
def home():
    names, rolls, times, l = extract_attendance()
    return render_template('home.html', names=names, rolls=rolls, times=times, l=l,
                           totalreg=totalreg(), datetoday2=datetoday2)

@app.route('/start', methods=['GET'])
def start():
    known_encodings, known_names = encode_known_faces()
    if not known_encodings:
        return render_template('home.html', totalreg=totalreg(), datetoday2=datetoday2,
                               mess='No registered faces found. Please add new faces first.')

    cap = cv2.VideoCapture(MOBILE_CAM_IP)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.45)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]
                add_attendance(name)

            top, right, bottom, left = top*4, right*4, bottom*4, left*4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow('Attendance', frame)
        if cv2.waitKey(1) == 27:  # ESC
            break
    cap.release()
    cv2.destroyAllWindows()

    names, rolls, times, l = extract_attendance()
    return render_template('home.html', names=names, rolls=rolls, times=times, l=l,
                           totalreg=totalreg(), datetoday2=datetoday2)

@app.route('/add', methods=['POST'])
def add():
    newusername = request.form['newusername']
    newuserid = request.form['newuserid']
    userimagefolder = f'static/faces/{newusername}_{newuserid}'
    os.makedirs(userimagefolder, exist_ok=True)

    cap = cv2.VideoCapture(MOBILE_CAM_IP)
    i = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        faces = extract_faces(frame)
        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 20), 2)
            cv2.putText(frame, f'Images Captured: {i}/50', (30, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 0, 20), 2)
            if i < 50:
                img_path = os.path.join(userimagefolder, f'{newusername}_{i}.jpg')
                cv2.imwrite(img_path, face_img)
                i += 1
        cv2.imshow('Adding New User', frame)
        key = cv2.waitKey(300)  # 300 ms delay between captures
        if key == 27 or i >= 50:  # ESC
            break
    cap.release()
    cv2.destroyAllWindows()

    names, rolls, times, l = extract_attendance()
    return render_template('home.html', names=names, rolls=rolls, times=times, l=l,
                           totalreg=totalreg(), datetoday2=datetoday2)

# ================== Run Server ==================

if __name__ == '__main__':
    app.run(debug=True)
