# 🏥 Healthcare Management System

## 📋 Description
The **Healthcare Management System** is a Flask-based web application that helps manage doctor and patient information, book appointments, and handle contact queries efficiently.  
It simplifies record keeping and improves communication between doctors and patients.

---

## ⚙️ Technologies Used
- **Python (Flask Framework)**
- **MySQL Database**
- **HTML, CSS, Bootstrap**
- **SQLAlchemy (ORM)**

---

## 🚀 Features
- User registration and login (for both **patients** and **doctors**)
- Doctor specialization and details
- Appointment booking and status update
- Contact form to send messages or feedback
- Separate access for doctors and patients
- Clean, responsive interface

---

## 🧠 How to Run the Project

### 1️⃣ Clone this repository
```bash
git clone https://github.com/shreyask17/Healthcare-Management-System.git
cd Healthcare-Management-System
```

### 2️⃣ Install the required libraries
```bash
Install the required libraries
```

### 3️⃣ Set up your MySQL database
- Open MySQL Workbench or any MySQL client.
- Create a database named healthcare_db.
- Update your MySQL username and password inside app.py here:
```bash
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Password@localhost/healthcare_db'
```

### 4️⃣ Run the application
```bash
http://127.0.0.1:5000/
```

⚠️ Note: Make sure your MySQL server is running before you start the Flask app.
