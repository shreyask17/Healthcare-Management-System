# 🏥 Healthcare Management System

*A Flask-based web application for managing doctors, patients, and appointments efficiently.*

---

## 📌 Project Overview

The **Healthcare Management System** is a web-based platform built with **Flask**, designed to simplify hospital operations.  
It allows patients to book appointments, doctors to manage schedules, and admins to monitor data — all through an easy-to-use dashboard.

---

## ⚙️ Features

* 👨‍⚕️ **Doctor Management** – Add, view, and remove doctors with specializations.  
* 🧑‍💼 **Patient Management** – Register and manage patient details.  
* 📅 **Appointment Booking** – Patients can book appointments with doctors.  
* 🔄 **Role-Based Access** – Separate dashboards for doctors and patients.  
* 📊 **Dynamic Dashboard** – Displays total doctors, patients, and appointments in real-time.  
* 🔐 **User Authentication** – Secure login and registration system using Flask-Login.  

---

## 🧠 Tech Stack

| Category | Technology |
|-----------|-------------|
| Backend | Flask (Python) |
| Frontend | HTML, CSS, Bootstrap |
| Database | MySQL |
| Authentication | Flask-Login |
| Version Control | Git & GitHub |

---

## 🚀 Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/Healthcare-Management-System.git
cd Healthcare-Management-System
```
2️⃣ Create Virtual Environment
```bash
python -m venv v_env
v_env\Scripts\activate   # On Windows
source v_env/bin/activate  # On macOS/Linux
```
3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
4️⃣ Configure Database
```bash
# In your .env file or config section, set your MySQL credentials

MYSQL_HOST=localhost
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=healthcare_db
```
5️⃣ Run the Application
```bash
python app.py
```
6️⃣ Access the Application
```bash
🏠 Home Page → http://127.0.0.1:5000/
🔐 Login → http://127.0.0.1:5000/login
🩺 Doctors → http://127.0.0.1:5000/doctors
👨‍⚕️ Patients → http://127.0.0.1:5000/patients
📅 Appointments → http://127.0.0.1:5000/appointments
```

---

🗂️ Project Structure
Healthcare-Management-System/
```bash
│
├── static/                  # CSS, JS, and images
├── templates/               # HTML templates (index, login, dashboard, etc.)
├── app.py                   # Main Flask application
├── models.py                # Database models
├── requirements.txt         # All dependencies
├── .env                     # Environment variables (DB credentials)
└── README.md                # Project documentation
```

---

💡 Note: Make sure your MySQL Workbench (or MySQL Server) is running in the background before starting the Flask app, otherwise the database connection will fail.
