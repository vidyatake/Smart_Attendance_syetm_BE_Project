# Smart Attendance System using Face Recognition

## 📌 Project Overview

The **Smart Attendance System** is a real-time face recognition based attendance management system developed using **Python and Flask**.
The system automatically detects and recognizes faces from a live video stream captured through an **IP camera** and marks attendance in a CSV file.

This project eliminates manual attendance processes and improves accuracy using **machine learning-based face recognition**.

---

## 🎯 Features

* Real-time face detection and recognition
* Automatic attendance marking
* Face registration system
* Captures multiple face samples for better accuracy
* Attendance stored in CSV format
* Web-based interface using Flask
* Works with mobile IP webcam

---

## 🛠 Technologies Used

* Python
* Flask
* OpenCV
* face_recognition (dlib)
* NumPy
* Pandas
* Haar Cascade Classifier

---

## ⚙ System Architecture

1. The system captures live video from an **IP camera**.
2. Faces are detected using **Haar Cascade Classifier**.
3. Detected faces are encoded using the **face_recognition library**.
4. The system compares captured faces with stored face encodings.
5. If a match is found, attendance is marked in the **CSV file with date and time**.
6. The Flask web interface allows users to:

   * Register new faces
   * Start attendance
   * View attendance records

---

## 📂 Project Structure

```
Smart-Attendance-System
│
├── static/
│   └── images
│
├── templates/
│   └── index.html
│
├── Attendance/
│   └── Attendance.csv
│
├── faces/
│   └── registered face images
│
├── app.py
├── haarcascade_frontalface_default.xml
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

### 1️⃣ Clone the Repository

```
git clone https://github.com/your-username/repository-name.git
```

### 2️⃣ Navigate to Project Folder

```
cd repository-name
```

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

## ▶ Running the Application

Run the Flask application:

```
python app.py
```

Open the browser and go to:

```
http://127.0.0.1:5000
```

---

## 📷 Face Registration

* Enter the user's name.
* The system captures **50 face images slowly** to improve recognition accuracy.
* Press **ESC** to stop capturing images.

---

## 📊 Attendance System

* When a registered face is detected:

  * Name is identified
  * Date and time are recorded
  * Attendance is stored in **CSV format**

---

## 📌 Future Improvements

* Database integration (MySQL / MongoDB)
* Mobile application support
* Multiple camera support
* Cloud-based attendance storage
* Dashboard with analytics

---

## 👨‍💻 Author

Developed by **BE Computer Engineering Student**
Vidya Take 
Shivani Tuplondhe

---

## 📄 License

This project is open-source and available for educational purposes.
